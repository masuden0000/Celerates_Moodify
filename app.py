from datetime import datetime

import streamlit as st

from src.core.ai_agent import setup_ai_agent
from src.core.utils import get_ai_response, initialize_session_state, process_user_input
from src.data.data_manager import load_music_data
from src.ui.sidebar import (
    export_chat_history,
    handle_sidebar_actions,
    initialize_chat_history,
    render_sidebar,
    sync_current_chat,
)

# Import all modules
from src.ui.styles import load_custom_css
from src.ui.ui_components import render_statistics

# =============================================================================
# MAIN APPLICATION
# =============================================================================

st.set_page_config(
    page_title="Moodify AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Main application function with minimalist design"""

    # Initialize chat history first
    initialize_chat_history()

    # Handle sidebar actions
    handle_sidebar_actions()

    # Handle export download
    if "export_data" in st.session_state:
        st.download_button(
            label="📁 Download Chat History",
            data=st.session_state.export_data,
            file_name=f"moodify_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="download_export",
        )
        del st.session_state.export_data

    # Render sidebar
    render_sidebar()

    # Main content
    with st.container():
        st.markdown(
            """        <div style="text-align: center; padding: 2rem 1rem;">
            <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; color: #111827;">
                💭 Moodify AI
            </h1>
            <p style="font-size: 1.1rem; color: #4B5563; max-width: 700px; margin: auto;">
                Halo! Selamat datang di <strong>Moodify</strong> — AI assistant musik yang siap nemenin kamu! 🎧<br>
            </p>
            <p style="font-size: 0.95rem; color: #6B7280; margin-top: 1rem;">
                Contoh: <em>"Lagi sedih nih", "mau lagu buat workout", "analisis musik happy",</em> atau <em>"siapa itu Taylor Swift?"</em> 🎶
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )  # Initialize
    initialize_session_state()
    load_custom_css()  # Load data and setup agent
    if st.session_state.df is None:
        with st.spinner("Loading database musik..."):
            st.session_state.df = load_music_data()

    if st.session_state.agent is None:
        with st.spinner("Setting up AI assistant..."):
            st.session_state.agent = setup_ai_agent(st.session_state.df)

    df = st.session_state.df
    agent = st.session_state.agent

    # Display messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">{message["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="bot-message">{message["content"]}</div>',
                unsafe_allow_html=True,
            )

    # Chat input
    user_input = st.chat_input("Cerita mood kamu atau tanya tentang musik...")
    if user_input:
        process_user_input(user_input, agent, df)
        # Sync with current chat after new message
        sync_current_chat()  # Statistics
    st.markdown("---")
    render_statistics(df)


if __name__ == "__main__":
    main()
