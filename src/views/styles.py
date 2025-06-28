"""
Styles - CSS and visual styling definitions
Manages application appearance and theme
"""

import streamlit as st

# MINIMALIST STYLING

def load_custom_css():
    """Load minimal, clean CSS styling"""
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Reset */
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main App Background */
    .stApp {
        background: #fafafa;
        color: #1a1a1a;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 300;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-header .subtitle {
        font-size: 1rem;
        color: #666;
        font-weight: 400;
    }
    
    /* Chat Messages */
    .user-message {
        background: #1a1a1a;
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 18px;
        margin: 1rem 0 1rem 25%;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .bot-message {
        background: white;
        color: #1a1a1a;
        padding: 1rem 1.25rem;
        border-radius: 18px;
        margin: 1rem 25% 1rem 0;
        border: 1px solid #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    /* Song Cards */
    .song-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 25% 0.75rem 0;
        transition: all 0.2s ease;
    }
    
    .song-card:hover {
        border-color: #1a1a1a;
        transform: translateY(-1px);
    }
    
    .song-title {
        font-size: 1.1rem;
        font-weight: 500;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .song-artist {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 1rem;
    }
    
    .song-stats {
        display: flex;
        gap: 1rem;
        font-size: 0.8rem;
    }
    
    .stat-badge {
        background: #f5f5f5;        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        color: #666;
        border: 1px solid #e0e0e0;
    }
    
    /* Statistics */
    .stats-container {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 2rem;
        text-align: center;
    }
    
    .stat-item {
        padding: 0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 300;
        color: #1a1a1a;
        display: block;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Chat Input Styling */
    .stChatInput > div > div > div > div {
        border-radius: 25px !important;
        border: 1px solid #e0e0e0 !important;
        background: white !important;
    }
    
    .stChatInput input {
        font-size: 0.9rem !important;
        padding: 0.75rem 1rem !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        color: #1a1a1a;
        font-weight: 400;
        transition: all 0.2s ease;
        width: 100%;
        padding: 0.75rem;
    }
    
    .stButton > button:hover {
        border-color: #1a1a1a;
        background: #f9f9f9;
        color: #1a1a1a;
    }
    
    /* Main content buttons - ensure they override sidebar styling */
    .stMain .stButton > button,
    .main .stButton > button {
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
        font-weight: 400 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        padding: 0.75rem !important;
    }
    
    .st-emotion-cache-1t02cvl {
        display: none;
    }
    
    .stMain .stButton > button:hover,
    .main .stButton > button:hover {
        border-color: #1a1a1a !important;
        background: #f9f9f9 !important;
        color: #1a1a1a !important;
    }
    
    /* Spinner */
    .stSpinner > div > div {
        border-color: #1a1a1a !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #e0e0e0;
        margin: 2rem 0;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .user-message, .bot-message, .song-card {
            margin-left: 1rem;
            margin-right: 1rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
    }    
    /* ========================================
       SIDEBAR STYLES - ChatGPT Like
    ======================================== */
    
    /* Streamlit Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc, .css-1y4p8pa {
        background-color: #171717 !important;
        color: #ececec !important;
    }
    
    /* Sidebar content */
    .css-17eq0hr {
        background-color: #171717 !important;
        color: #ececec !important;
    }
    
    /* Sidebar buttons */
    .st-emotion-cache-13kn1tw {
    display: none;
    width: 0%;
    }
    
    .st-emotion-cache-1jw38fe {
    width: 100%;
    }
    
    .e1quxfqw8 {
    display: none;
    }
      /* Sidebar buttons - ONLY apply to sidebar */
    .stSidebar .stButton button {
        background-color: #202123 !important;
        color: #ececec !important;
        border: 1px solid #363636 !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }
    
    .stSidebar .stButton button:hover {
        background-color: #40414f !important;
        border-color: #565869 !important;
    }
    
    .stSidebar .stButton button[kind="primary"] {
        background-color: #343541 !important;
        border-color: #565869 !important;
    }
    
    .stSidebar .stButton button[kind="primary"]:hover {
        background-color: #40414f !important;
    }
    
    /* Sidebar text */
    .css-17eq0hr h3 {
        color: #ececec !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .css-17eq0hr p, .css-17eq0hr div {
        color: #ececec !important;
    }
    
    /* Sidebar markdown */
    .css-17eq0hr .markdown-text-container {
        color: #ececec !important;
    }
    
    /* Info boxes in sidebar */
    .css-17eq0hr .element-container .stAlert {
        background-color: #2a2b32 !important;
        color: #ececec !important;
        border: 1px solid #363636 !important;
    }
    
    /* Warning boxes in sidebar */
    .css-17eq0hr .element-container .stWarning {
        background-color: #dc3545 !important;
        color: #ffffff !important;
        border: 1px solid #dc3545 !important;
    }
    
    /* CRITICAL: Ensure main content buttons are NOT affected by sidebar styling */
    .stMain .stButton button,
    .main .stButton button,
    div[data-testid="stMain"] .stButton button,
    section[data-testid="stMain"] .stButton button {
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
        font-weight: 400 !important;
        transition: all 0.2s ease !important;
        padding: 0.75rem !important;
    }
    
    .stMain .stButton button:hover,
    .main .stButton button:hover,
    div[data-testid="stMain"] .stButton button:hover,
    section[data-testid="stMain"] .stButton button:hover {
        border-color: #1a1a1a !important;
        background: #f9f9f9 !important;
        color: #1a1a1a !important;
    }
    
    /* Sidebar scrollbar */
    .css-17eq0hr::-webkit-scrollbar {
        width: 4px;
    }
    
    .css-17eq0hr::-webkit-scrollbar-track {
        background: #171717;
    }
    
    .css-17eq0hr::-webkit-scrollbar-thumb {
        background: #4a4a4a;
        border-radius: 2px;
    }
    
    .css-17eq0hr::-webkit-scrollbar-thumb:hover {
        background: #5a5a5a;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
