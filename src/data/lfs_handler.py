import streamlit as st
import pandas as pd
import os
import requests
from io import StringIO

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

@st.cache_data
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
