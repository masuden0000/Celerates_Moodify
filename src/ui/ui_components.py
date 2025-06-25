from typing import Dict

import pandas as pd
import streamlit as st

# =============================================================================
# MINIMALIST UI COMPONENTS
# =============================================================================

def render_statistics(df: pd.DataFrame):
    """Render minimalist app statistics"""
    analytics = st.session_state.get(
        "analytics", {"total_queries": 0, "recommendations_given": 0}
    )

    st.markdown(
        f"""
    <div class="stats-container">
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-value">{len(df):,}</span>
                <div class="stat-label">Songs</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{df['artist_name'].nunique():,}</span>
                <div class="stat-label">Artists</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{df['genre'].nunique():,}</span>
                <div class="stat-label">Genres</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{analytics['total_queries']:,}</span>
                <div class="stat-label">Queries</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
