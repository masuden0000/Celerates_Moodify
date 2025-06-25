from typing import Dict

import pandas as pd
import streamlit as st

# =============================================================================
# MINIMALIST UI COMPONENTS
# =============================================================================

def render_mood_buttons():
    """Render minimalist mood selection buttons"""
    st.markdown('<div class="mood-buttons">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    buttons = [
        ("😊 Happy", "Lagi mood happy nih, kasih lagu yang upbeat!", col1),
        ("😢 Sad", "Lagi sedih, mau lagu yang emotional", col2),
        ("😌 Santai", "Mood lagi santai, mau yang chill", col3),
        ("🔍 Analisis", "Analisis musik happy", col4),
    ]

    for label, prompt, col in buttons:
        with col:
            if st.button(label, key=f"mood_{label}", use_container_width=True):
                return prompt

    st.markdown("</div>", unsafe_allow_html=True)
    return None


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
