"""
LFS handler - Git Large File Storage utilities
Handles large file operations and storage management
"""

import os
import subprocess
from io import StringIO

import pandas as pd
import requests
import streamlit as st

def download_from_github_lfs(repo_owner, repo_name, file_path):
    """Download LFS file directly from GitHub"""

    # GitHub LFS media URL format
    lfs_url = f"https://media.githubusercontent.com/media/{repo_owner}/{repo_name}/main/{file_path}"

    try:
        response = requests.get(lfs_url)
        if response.status_code == 200:
            return StringIO(response.text)
        else:
            st.error(f"Failed to download from GitHub LFS. Status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error downloading from GitHub LFS: {str(e)}")
        return None

def check_lfs_file_status(file_path):
    """Check if file is LFS pointer and handle download with git lfs pull"""

    if not os.path.exists(file_path):
        return False, "File not found"

    file_size = os.path.getsize(file_path)

    # LFS pointer files are typically very small (< 1KB)
    if file_size < 1000:
        st.info("📥 Detecting Git LFS pointer file. Attempting download...")

        try:
            # Check if git lfs is installed
            lfs_check = subprocess.run(
                ["git", "lfs", "version"], capture_output=True, text=True
            )

            if lfs_check.returncode != 0:
                return False, "Git LFS not installed"

            # Pull LFS files
            result = subprocess.run(
                ["git", "lfs", "pull"], capture_output=True, text=True, cwd="."
            )

            if result.returncode != 0:
                return False, f"Git LFS pull failed: {result.stderr}"

            # Check if file size increased after pull
            new_size = os.path.getsize(file_path)
            if new_size > file_size:
                size_mb = new_size / (1024 * 1024)
                st.success(
                    f"✅ Git LFS file downloaded successfully! Size: {size_mb:.1f} MB"
                )
                return True, f"Downloaded {size_mb:.1f} MB"
            else:
                return False, "File download may have failed - size unchanged"

        except FileNotFoundError:
            return False, "Git command not found"
        except Exception as e:
            return False, f"Error during LFS pull: {str(e)}"

    # File is already the correct size
    size_mb = file_size / (1024 * 1024)
    return True, f"File ready ({size_mb:.1f} MB)"

@st.cache_data
def load_spotify_data():
    """Load spotify data with LFS support - Enhanced version"""

    file_path = "spotify_data.csv"

    # Check if file exists
    if not os.path.exists(file_path):
        st.error("spotify_data.csv not found!")
        return None

    # Check if file is LFS pointer (small file)
    file_size = os.path.getsize(file_path)

    if file_size < 1000:  # LFS pointer files are very small
        st.info("📥 Downloading large file via Git LFS...")
        try:
            # Pull LFS files
            result = subprocess.run(
                ["git", "lfs", "pull"], capture_output=True, text=True, cwd="."
            )
            if result.returncode != 0:
                st.error(f"Git LFS pull failed: {result.stderr}")
                return None
            else:
                st.success("✅ Git LFS pull completed successfully!")
        except Exception as e:
            st.error(f"Error pulling LFS files: {str(e)}")
            return None

    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        file_size_mb = file_size / (1024 * 1024)
        st.success(
            f"✅ Data loaded successfully! Shape: {df.shape} | Size: {file_size_mb:.1f} MB"
        )
        return df
    except Exception as e:
        st.error(f"❌ Error loading CSV: {str(e)}")
        return None

def load_spotify_data_with_fallback():
    """Load data with multiple fallback methods"""
    
    file_path = "spotify_data.csv"
    
    # Method 1: Try local file
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            file_size = os.path.getsize(file_path)
            
            # Check if it's actual data, not LFS pointer
            if len(df) > 1000 and file_size > 1000:  
                st.success(f"✅ Data loaded from local file! Shape: {df.shape}")
                return df
            else:
                st.info("📝 Local file appears to be LFS pointer, trying GitHub LFS...")
        except Exception as e:
            st.warning(f"⚠️ Error reading local file: {str(e)}")
    
    # Method 2: Try GitHub LFS direct download
    st.info("📥 Downloading data from GitHub LFS...")
    csv_buffer = download_from_github_lfs("masuden0000", "Celerates_Moodify", "spotify_data.csv")
    
    if csv_buffer:
        try:
            df = pd.read_csv(csv_buffer)
            st.success(f"✅ Data loaded from GitHub LFS! Shape: {df.shape}")
            return df
        except Exception as e:
            st.error(f"❌ Error parsing CSV from GitHub LFS: {str(e)}")
    
    # Method 3: Error state
    st.error("❌ Unable to load Spotify data from any source")
    st.info("🔧 Available fallback options:")
    st.info("- Check if Git LFS is properly configured")
    st.info("- Verify GitHub repository access")
    st.info("- Consider using alternative data sources")
    
    return None

def get_file_info(df):
    """Get file information for display"""
    if df is not None:
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum() / (1024 * 1024),  # MB
            "sample_data": df.head()
        }
    return None
