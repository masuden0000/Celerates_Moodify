import json
from datetime import datetime
from typing import Dict, List

import streamlit as st

# =============================================================================
# SIDEBAR COMPONENTS - Enhanced Beautiful Version
# =============================================================================

# Custom CSS for better styling
def inject_sidebar_css():
    """Inject custom CSS for beautiful sidebar styling"""
    st.markdown("""
    <style>
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Chat item styling */
    .chat-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px;
        margin: 4px 0;
        border-left: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    .chat-item:hover {
        background: rgba(255, 255, 255, 0.2);
        border-left: 3px solid #4CAF50;
        transform: translateX(2px);
    }
    
    .chat-item.active {
        background: rgba(76, 175, 80, 0.2);
        border-left: 3px solid #4CAF50;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Chat title styling */
    .chat-title {
        font-size: 0.9rem;
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 2px;
    }
    
    .chat-date {
        font-size: 0.75rem;
        color: #7f8c8d;
        opacity: 0.8;
    }
    
    /* Header styling */
    .sidebar-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
        font-weight: bold;
    }
    
    /* Divider styling */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 15px 0;
        border: none;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 8px;
    }
    
    .status-active {
        background: #4CAF50;
        color: white;
    }
    
    .status-recent {
        background: #FF9800;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


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
            # Use first 35 characters for better readability
            if len(title) > 35:
                title = title[:35] + "..."

            # Update session state
            if chat_id in st.session_state.chat_sessions:
                st.session_state.chat_sessions[chat_id]["title"] = title
                st.session_state.chat_sessions[chat_id]["updated_at"] = datetime.now().isoformat()


def switch_chat(chat_id: str):
    """Switch to a different chat session"""
    if chat_id in st.session_state.chat_sessions:
        # Save current messages to current chat
        if st.session_state.current_chat_id in st.session_state.chat_sessions:
            st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"] = st.session_state.messages

        # Switch to new chat
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = st.session_state.chat_sessions[chat_id]["messages"].copy()


def delete_chat(chat_id: str):
    """Delete a chat session"""
    if chat_id in st.session_state.chat_sessions and len(st.session_state.chat_sessions) > 1:
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


def format_chat_date(date_str: str) -> str:
    """Format chat date for display"""
    try:
        created_date = datetime.fromisoformat(date_str)
        now = datetime.now()
        
        if created_date.date() == now.date():
            return f"Today {created_date.strftime('%H:%M')}"
        elif created_date.date() == (now.date() - timedelta(days=1)):
            return f"Yesterday {created_date.strftime('%H:%M')}"
        elif (now - created_date).days < 7:
            return created_date.strftime('%A %H:%M')
        else:
            return created_date.strftime('%m/%d/%y')
    except:
        return "Recent"


def render_chat_item(chat_id: str, chat_data: Dict, is_active: bool):
    """Render individual chat item with beautiful styling"""
    # Format date
    date_str = format_chat_date(chat_data["created_at"])
    
    # Determine status
    message_count = len(chat_data.get("messages", []))
    
    # Create container with custom styling
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Chat title and info
            if is_active:
                st.markdown(f"""
                <div class="chat-item active">
                    <div class="chat-title">🎵 {chat_data['title']}</div>
                    <div class="chat-date">{date_str} • {message_count} msgs</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(
                    f"🎵 {chat_data['title']}\n{date_str} • {message_count} msgs",
                    key=f"chat_btn_{chat_id}",
                    help=f"Switch to chat created on {date_str}",
                    use_container_width=True
                ):
                    switch_chat(chat_id)
                    st.rerun()
        
        with col2:
            # Delete button (only show if more than 1 chat)
            if len(st.session_state.chat_sessions) > 1:
                if st.button("🗑️", key=f"del_{chat_id}", help="Delete this chat"):
                    delete_chat(chat_id)
                    st.rerun()


def render_sidebar():
    """Render beautiful sidebar with enhanced styling"""
    
    # Inject custom CSS
    inject_sidebar_css()
    
    # Initialize chat history
    initialize_chat_history()

    # Render sidebar using Streamlit's native sidebar
    with st.sidebar:
        # Beautiful header
        st.markdown("""
        <div class="sidebar-header">
            <h2>🎧 Moodify Chat</h2>
            <p style="margin: 0; opacity: 0.9;">Your Music Mood Assistant</p>
        </div>
        """, unsafe_allow_html=True)

        # New Chat Button with enhanced styling
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("✨ Start New Chat", use_container_width=True, type="primary"):
                new_chat_id = create_new_chat()
                switch_chat(new_chat_id)
                st.rerun()
        
        with col2:
            # Chat count badge
            chat_count = len(st.session_state.chat_sessions)
            st.markdown(f"""
            <div style="background: #4CAF50; color: white; text-align: center; 
                        border-radius: 20px; padding: 8px; font-size: 0.8rem; font-weight: bold;">
                {chat_count}
            </div>
            """, unsafe_allow_html=True)

        # Custom divider
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        if st.button("📊 View Statistic"):
         st.session_state.show_stats = True

        if st.button("❌ Hide Statistic"):
         st.session_state.show_stats = False
         
        # Chat History Section
        if st.session_state.chat_sessions:
            st.markdown("### 💬 Recent Conversations")
            
            # Sort chats by updated_at (most recent first)
            sorted_chats = sorted(
                st.session_state.chat_sessions.items(),
                key=lambda x: x[1]["updated_at"],
                reverse=True,
            )
    
    

            # Render each chat item
        for chat_id, chat_data in sorted_chats:
                is_active = chat_id == st.session_state.current_chat_id
                render_chat_item(chat_id, chat_data, is_active)
                
                # Add subtle spacing
                st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)

        else:
            # Empty state with encouragement
            st.markdown("""
            <div style="text-align: center; padding: 20px; color: #7f8c8d;">
                <h4>🎵 No conversations yet!</h4>
                <p>Start chatting to discover your perfect music mood</p>
            </div>
            """, unsafe_allow_html=True)

        # Custom divider
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        # Action Buttons Section
        st.markdown("### ⚙️ Actions")
        
        col1, col2 = st.columns(2)

        with col1:
            # Export button
            if st.button("📥 Export", use_container_width=True, help="Export chat history"):
                try:
                    export_data = export_chat_history()
                    filename = f"moodify_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

                    st.download_button(
                        label="💾 Download",
                        data=export_data,
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True,
                    )
                    st.success("✅ Ready to download!")
                except Exception as e:
                    st.error(f"❌ Export failed: {str(e)}")

        with col2:
            # Clear all button
            if st.button("🧹 Clear All", use_container_width=True, help="Clear all chats"):
                if st.session_state.get("confirm_clear", False):
                    clear_all_history()
                    st.session_state.confirm_clear = False
                    st.success("✅ All chats cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.rerun()

        # Confirmation dialog
        if st.session_state.get("confirm_clear", False):
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; 
                        border-radius: 8px; padding: 12px; margin: 10px 0;">
                <strong>⚠️ Confirm Action</strong><br>
                <small>This will delete all your chat history permanently.</small>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Confirm", use_container_width=True, type="primary"):
                    clear_all_history()
                    st.session_state.confirm_clear = False
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.confirm_clear = False
                    st.rerun()

        # Footer info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #7f8c8d; font-size: 0.8rem;">
            <p>🎵 Powered by Moodify AI<br>
            <small>Find your perfect music mood</small></p>
        </div>
        """, unsafe_allow_html=True)


def handle_sidebar_actions():
    """Handle sidebar actions - simplified for native Streamlit"""
    # Actions are handled directly in render_sidebar()
    pass


def sync_current_chat():
    """Sync current messages with current chat session"""
    if st.session_state.current_chat_id in st.session_state.chat_sessions:
        # Update current chat with messages
        current_messages = st.session_state.messages
        st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"] = current_messages

        # Update title if this is the first message or still "New Chat"
        current_title = st.session_state.chat_sessions[st.session_state.current_chat_id]["title"]
        if len(current_messages) > 0 and current_title == "New Chat":
            update_chat_title(st.session_state.current_chat_id, current_messages)


# Additional utility functions for enhanced experience
def get_chat_stats():
    """Get statistics about chat sessions"""
    if not st.session_state.chat_sessions:
        return {"total_chats": 0, "total_messages": 0, "most_active_chat": None}
    
    total_messages = sum(len(chat["messages"]) for chat in st.session_state.chat_sessions.values())
    most_active_chat = max(
        st.session_state.chat_sessions.items(),
        key=lambda x: len(x[1]["messages"]),
        default=(None, None)
    )[1]
    
    return {
        "total_chats": len(st.session_state.chat_sessions),
        "total_messages": total_messages,
        "most_active_chat": most_active_chat
    }


def render_chat_stats():
    """Render chat statistics in a beautiful way"""
    stats = get_chat_stats()
    
    if stats["total_chats"] > 0:
        st.markdown("### 📊 Your Chat Stats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="💬 Total Chats",
                value=stats["total_chats"],
                help="Total number of conversations"
            )
        
        with col2:
            st.metric(
                label="💌 Messages",
                value=stats["total_messages"],
                help="Total messages exchanged"
            )
        
        with col3:
            if stats["most_active_chat"]:
                active_count = len(stats["most_active_chat"]["messages"])
                st.metric(
                    label="🔥 Most Active",
                    value=f"{active_count} msgs",
                    help="Most active conversation"
                )

# Import missing timedelta
from datetime import timedelta