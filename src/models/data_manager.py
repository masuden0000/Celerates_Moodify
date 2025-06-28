"""
Data manager - Music dataset loading and management
Handles CSV data loading and preprocessing
"""

import os
import subprocess
import time
from functools import wraps

import numpy as np
import pandas as pd
import streamlit as st

from .lfs_handler import (
    check_lfs_file_status,
    load_spotify_data,
    load_spotify_data_with_fallback,
)

# PERFORMANCE MONITORING

def monitor_performance(func):
    """Decorator to monitor function execution time"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        if execution_time > 5:  # Only show if > 5 seconds
            st.info(f"⏱️ {func.__name__} completed in {execution_time:.2f} seconds")

        return result

    return wrapper

# DATA MANAGEMENT

@monitor_performance
@st.cache_data(
    ttl=3600, show_spinner=False
)  # Cache for 1 hour, disable default spinner
def load_music_data():
    """Optimized spotify data loading with enhanced performance"""

    # First check session state cache
    cached_data = get_cached_data()
    if cached_data is not None:
        return cached_data

    file_path = "spotify_data.csv"

    # Quick existence check
    if not os.path.exists(file_path):
        st.error("❌ spotify_data.csv not found!")
        return None

    # Check file size and LFS status
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)

    # Handle LFS files (< 1KB indicates LFS pointer)
    if file_size < 1024:
        st.info("📥 LFS file detected. Downloading...")

        with st.spinner("Downloading data via Git LFS..."):
            try:
                # Use timeout to prevent hanging
                result = subprocess.run(
                    ["git", "lfs", "pull"],
                    capture_output=True,
                    text=True,
                    cwd=".",
                    timeout=60,
                )

                if result.returncode == 0:
                    # Refresh file size after download
                    file_size = os.path.getsize(file_path)
                    file_size_mb = file_size / (1024 * 1024)
                    st.success(
                        f"✅ LFS download completed! Size: {file_size_mb:.1f} MB"
                    )
                else:
                    st.error(f"❌ Git LFS failed: {result.stderr}")
                    return None

            except subprocess.TimeoutExpired:
                st.error("⏰ LFS download timeout (60s)")
                return None
            except Exception as e:
                st.error(f"❌ LFS error: {str(e)}")
                return None

    # Optimized CSV loading (silent mode)
    try:
        # Optimized pandas parameters for performance
        df = pd.read_csv(
            file_path,
            engine="c",  # Use fast C engine
            low_memory=False,  # Read entire file at once
            na_filter=True,  # Handle NaN values efficiently
            verbose=False,  # Reduce output
            encoding="utf-8",  # Explicit encoding
        )

        # Process data silently
        processed_df = process_music_data(df)

        # Cache the processed data
        set_cached_data(processed_df)

        return processed_df

    except pd.errors.EmptyDataError:
        st.error("❌ CSV file is empty")
        return None
    except pd.errors.ParserError as e:
        st.error(f"❌ CSV parsing error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error loading CSV: {str(e)}")
        return None

# UTILITY FUNCTIONS

def get_data_info(df):
    """Get comprehensive data information for debugging"""
    if df is None:
        return "No data loaded"

    info = {
        "shape": df.shape,
        "memory_usage_mb": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f}",
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
    }

    return info

def process_music_data(df):
    """Optimized processing and enhancement of music data"""

    # Validate required columns exist
    required_cols = ["valence", "energy"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.warning(f"⚠️ Missing columns: {missing_cols}. Skipping mood classification.")
        return df

    # Optimized mood classification using vectorized operations
    # Instead of apply(), use numpy conditions for better performance
    conditions = [
        (df["valence"] >= 0.6) & (df["energy"] >= 0.6),
        (df["valence"] <= 0.4) | (df["energy"] <= 0.3),
    ]
    choices = ["happy", "sad"]

    df["mood"] = np.select(conditions, choices, default="neutral")

    # Optimized duration conversion (vectorized)
    if "duration_ms" in df.columns:
        df["duration_min"] = (df["duration_ms"] / 60000).round(2)

    # Optional: Data type optimization to reduce memory usage
    # Convert object columns to category if they have limited unique values
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].nunique() / len(df) < 0.5:  # If less than 50% unique values
            df[col] = df[col].astype("category")

    return df

# SESSION STATE OPTIMIZATION

def get_cached_data():
    """Get data from session state cache if available"""
    if "music_data_cache" in st.session_state:
        cache_time = st.session_state.get("music_data_cache_time", 0)
        current_time = time.time()

        # Cache valid for 1 hour (3600 seconds)
        if current_time - cache_time < 3600:
            st.info("📦 Using cached data from session...")
            return st.session_state.music_data_cache

    return None

def set_cached_data(df):
    """Cache data in session state"""
    st.session_state.music_data_cache = df
    st.session_state.music_data_cache_time = time.time()
