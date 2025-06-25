import json
from datetime import datetime
from typing import Dict, List

import streamlit as st

# =============================================================================
# SIDEBAR COMPONENTS - ChatGPT Style
# =============================================================================


def initialize_chat_history():
    """Initialize chat history in session state"""
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}

    if "current_chat_id" not in st.session_state:
        # Create first chat session
        new_chat_id = create_new_chat()
        st.session_state.current_chat_id = new_chat_id


def create_new_chat() -> str:
    """Create a new chat session and return its ID"""
    chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.chat_sessions[chat_id] = {
        "id": chat_id,
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    return chat_id


def update_chat_title(chat_id: str, messages: List[Dict]):
    """Update chat title based on first user message"""
    if messages and len(messages) > 0:
        # Find first user message
        first_user_message = None
        for msg in messages:
            if msg.get("role") == "user":
                first_user_message = msg.get("content", "")
                break

        if first_user_message:
            # Clean and format title
            title = first_user_message.strip()
            # Remove common prefixes if any
            title = title.replace("Lagi mood ", "").replace("Mau lagu ", "")
            # Use first 40 characters for better readability
            if len(title) > 40:
                title = title[:40] + "..."

            # Update session state
            if chat_id in st.session_state.chat_sessions:
                st.session_state.chat_sessions[chat_id]["title"] = title
                st.session_state.chat_sessions[chat_id][
                    "updated_at"
                ] = datetime.now().isoformat()


def switch_chat(chat_id: str):
    """Switch to a different chat session"""
    if chat_id in st.session_state.chat_sessions:
        # Save current messages to current chat
        if st.session_state.current_chat_id in st.session_state.chat_sessions:
            st.session_state.chat_sessions[st.session_state.current_chat_id][
                "messages"
            ] = st.session_state.messages

        # Switch to new chat
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = st.session_state.chat_sessions[chat_id][
            "messages"
        ].copy()


def delete_chat(chat_id: str):
    """Delete a chat session"""
    if (
        chat_id in st.session_state.chat_sessions
        and len(st.session_state.chat_sessions) > 1
    ):
        del st.session_state.chat_sessions[chat_id]

        # If deleted chat was current, switch to another one
        if st.session_state.current_chat_id == chat_id:
            remaining_chats = list(st.session_state.chat_sessions.keys())
            if remaining_chats:
                switch_chat(remaining_chats[0])


def clear_all_history():
    """Clear all chat history"""
    st.session_state.chat_sessions = {}
    new_chat_id = create_new_chat()
    st.session_state.current_chat_id = new_chat_id
    st.session_state.messages = []


def serialize_datetime_objects(obj):
    """Convert datetime objects to ISO format strings for JSON serialization"""
    if isinstance(obj, dict):
        return {key: serialize_datetime_objects(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime_objects(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


def export_chat_history() -> str:
    """Export all chat history as JSON"""
    # Deep copy and serialize datetime objects
    serialized_sessions = serialize_datetime_objects(st.session_state.chat_sessions)

    export_data = {
        "export_date": datetime.now().isoformat(),
        "chat_sessions": serialized_sessions,
        "total_sessions": len(st.session_state.chat_sessions),
    }
    return json.dumps(export_data, indent=2, ensure_ascii=False)


def render_sidebar():
    """Render ChatGPT-like sidebar using Streamlit native components"""

    # Initialize chat history
    initialize_chat_history()

    # Render sidebar using Streamlit's native sidebar
    with st.sidebar:
        st.markdown(" 🕜 Chat History")

        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="secondary"):
            new_chat_id = create_new_chat()
            switch_chat(new_chat_id)
            st.rerun()

        st.markdown("---")

        # Chat History List
        if st.session_state.chat_sessions:
            # Sort chats by updated_at (most recent first)
            sorted_chats = sorted(
                st.session_state.chat_sessions.items(),
                key=lambda x: x[1]["updated_at"],
                reverse=True,
            )

            st.markdown("**Recent Conversations:**")

            for chat_id, chat_data in sorted_chats:
                is_active = chat_id == st.session_state.current_chat_id

                # Format date
                try:
                    created_date = datetime.fromisoformat(chat_data["created_at"])
                    if created_date.date() == datetime.now().date():
                        date_str = created_date.strftime("%H:%M")
                    else:
                        date_str = created_date.strftime("%m/%d")
                except:
                    date_str = "Recent"

                # Create chat item container
                chat_container = st.container()
                with chat_container:
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        # Chat title button
                        button_type = "primary" if is_active else "secondary"
                        if st.button(
                            f"💬 {chat_data['title']}",
                            key=f"chat_{chat_id}",
                            help=f"Created: {date_str}",
                            type=button_type,
                            use_container_width=True,
                        ):
                            if not is_active:
                                switch_chat(chat_id)
                                st.rerun()

                    with col2:
                        # Delete button
                        if len(st.session_state.chat_sessions) > 1:
                            if st.button(
                                "🗑️", key=f"delete_{chat_id}", help="Delete chat"
                            ):
                                delete_chat(chat_id)
                                st.rerun()

                # Add some spacing
                st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.info("No conversations yet. Start a new chat!")

        st.markdown("---")

        # Action Buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "📁 Export", use_container_width=True, help="Export chat history"
            ):
                try:
                    export_data = export_chat_history()
                    # Create filename with current date
                    filename = f"moodify_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

                    # Provide download button
                    st.download_button(
                        label="💾 Download JSON",
                        data=export_data,
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True,
                    )
                    st.success("✅ Chat history ready for download!")
                except Exception as e:
                    st.error(f"❌ Export failed: {str(e)}")

        with col2:
            if st.button(
                "🗑️ Clear All", use_container_width=True, help="Clear all chat history"
            ):
                if st.session_state.get("confirm_clear", False):
                    clear_all_history()
                    st.session_state.confirm_clear = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.rerun()

        # Confirmation message for clear all
        if st.session_state.get("confirm_clear", False):
            st.warning(
                "⚠️ Click 'Clear All' again to confirm deletion of all chat history."
            )
            if st.button("Cancel", key="cancel_clear"):
                st.session_state.confirm_clear = False
                st.rerun()


def handle_sidebar_actions():
    """Handle sidebar actions - simplified for native Streamlit"""
    # Actions are handled directly in render_sidebar()
    pass


def sync_current_chat():
    """Sync current messages with current chat session"""
    if st.session_state.current_chat_id in st.session_state.chat_sessions:
        # Update current chat with messages
        current_messages = st.session_state.messages
        st.session_state.chat_sessions[st.session_state.current_chat_id][
            "messages"
        ] = current_messages

        # Update title if this is the first message or still "New Chat"
        current_title = st.session_state.chat_sessions[
            st.session_state.current_chat_id
        ]["title"]
        if len(current_messages) > 0 and current_title == "New Chat":
            update_chat_title(st.session_state.current_chat_id, current_messages)
