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
        background: #fafafa !important;
        color: #1a1a1a !important;
    }
    
    /* Main content area */
    .stMain, .main, [data-testid="stMain"] {
        background: #fafafa !important;
        color: #1a1a1a !important;
    }
    
    /* Override dark theme if applied */
    .stApp[data-theme="dark"] {
        background: #fafafa !important;
        color: #1a1a1a !important;
    }
    
    .stMain[data-theme="dark"], .main[data-theme="dark"], [data-testid="stMain"][data-theme="dark"] {
        background: #fafafa !important;
        color: #1a1a1a !important;
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
    }      /* Statistics */
    .stats-container {
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        margin: 2rem 0 !important;
    }
    
    .stats-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)) !important;
        gap: 2rem !important;
        text-align: center !important;
    }
    
    .stat-item {
        padding: 0 !important;
    }
    
    .stat-value {
        font-size: 2rem !important;
        font-weight: 300 !important;
        color: #000000 !important;
        display: block !important;
        text-shadow: none !important;
        -webkit-text-fill-color: #000000 !important;
        -moz-text-fill-color: #000000 !important;
    }
    
    .stat-label {
        font-size: 0.8rem !important;
        color: #333333 !important;
        margin-top: 0.25rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        text-shadow: none !important;
        -webkit-text-fill-color: #333333 !important;
        -moz-text-fill-color: #333333 !important;
    }
    
    /* Force dark text on statistics regardless of theme - Enhanced */
    [data-testid="stMarkdownContainer"] .stats-container .stat-value,
    .stMarkdown .stats-container .stat-value,
    .stats-container .stat-value,
    div[class*="stats-container"] .stat-value,
    .stApp .stats-container .stat-value {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        -moz-text-fill-color: #000000 !important;
        text-shadow: none !important;
    }
    
    [data-testid="stMarkdownContainer"] .stats-container .stat-label,
    .stMarkdown .stats-container .stat-label,
    .stats-container .stat-label,
    div[class*="stats-container"] .stat-label,
    .stApp .stats-container .stat-label {
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
        -moz-text-fill-color: #333333 !important;
        text-shadow: none !important;
    }
    
    /* Streamlit Metrics Styling - Force dark text with enhanced specificity */
    [data-testid="metric-container"],
    div[data-testid="metric-container"],
    .stMetric {
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"],
    div[data-testid="metric-container"] [data-testid="stMetricValue"],
    [data-testid="stMetricValue"],
    .stMetric [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 600 !important;
        text-shadow: none !important;
        -webkit-text-fill-color: #000000 !important;
        -moz-text-fill-color: #000000 !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricLabel"],
    div[data-testid="metric-container"] [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"],
    .stMetric [data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-weight: 500 !important;
        text-shadow: none !important;
        -webkit-text-fill-color: #333333 !important;
        -moz-text-fill-color: #333333 !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricDelta"],
    div[data-testid="metric-container"] [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"],
    .stMetric [data-testid="stMetricDelta"] {
        color: #28a745 !important;
        font-weight: 400 !important;
        text-shadow: none !important;
        -webkit-text-fill-color: #28a745 !important;
        -moz-text-fill-color: #28a745 !important;
    }
    
    /* Additional CSS to override any theme-based text color inheritance */
    .stApp[data-theme="dark"] .stats-container .stat-value,
    .stApp[data-theme="light"] .stats-container .stat-value,
    html[data-theme="dark"] .stats-container .stat-value,
    html[data-theme="light"] .stats-container .stat-value {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        -moz-text-fill-color: #000000 !important;
    }
    
    .stApp[data-theme="dark"] .stats-container .stat-label,
    .stApp[data-theme="light"] .stats-container .stat-label,
    html[data-theme="dark"] .stats-container .stat-label,
    html[data-theme="light"] .stats-container .stat-label {
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
        -moz-text-fill-color: #333333 !important;
    }
      /* Universal text color override for main content - Enhanced */
    .stMain *, .main *, [data-testid="stMain"] * {
        color: inherit !important;
    }
    
    .stMain h1, .stMain h2, .stMain h3, .stMain h4, .stMain h5, .stMain h6,
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
    [data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3, 
    [data-testid="stMain"] h4, [data-testid="stMain"] h5, [data-testid="stMain"] h6 {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        -moz-text-fill-color: #000000 !important;
    }
    
    .stMain p, .stMain div, .stMain span,
    .main p, .main div, .main span,
    [data-testid="stMain"] p, [data-testid="stMain"] div, [data-testid="stMain"] span {
        color: #1a1a1a !important;
        -webkit-text-fill-color: #1a1a1a !important;
        -moz-text-fill-color: #1a1a1a !important;
    }
    
    /* Additional browser compatibility fixes */
    .stMain .stMarkdown, .main .stMarkdown, [data-testid="stMain"] .stMarkdown {
        color: #1a1a1a !important;
        -webkit-text-fill-color: #1a1a1a !important;
        -moz-text-fill-color: #1a1a1a !important;
    }
    
    .stMain .stText, .main .stText, [data-testid="stMain"] .stText {
        color: #1a1a1a !important;
        -webkit-text-fill-color: #1a1a1a !important;
        -moz-text-fill-color: #1a1a1a !important;
    }
    
    /* Enhanced override for all text elements in info/success/warning/error containers */
    .stMain .stInfo, .stMain .stSuccess, .stMain .stWarning, .stMain .stError,
    .main .stInfo, .main .stSuccess, .main .stWarning, .main .stError,
    [data-testid="stMain"] .stInfo, [data-testid="stMain"] .stSuccess, 
    [data-testid="stMain"] .stWarning, [data-testid="stMain"] .stError {
        color: #1a1a1a !important;
        -webkit-text-fill-color: #1a1a1a !important;
        -moz-text-fill-color: #1a1a1a !important;
    }
    
    /* Fix for Plotly charts text color */
    .stMain .js-plotly-plot, .main .js-plotly-plot, [data-testid="stMain"] .js-plotly-plot {
        background: white !important;
    }
    
    /* Ensure white background for all content containers */
    .stMain .element-container, .main .element-container, [data-testid="stMain"] .element-container {
        background: transparent !important;
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
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        -moz-text-fill-color: #ffffff !important;
    }
    
    /* Additional chat input text color enforcement */
    .stChatInput input::placeholder {
        color: #ffffff !important;
        opacity: 0.7 !important;
        -webkit-text-fill-color: #ffffff !important;
        -moz-text-fill-color: #ffffff !important;
    }
    
    /* Force white text in chat input across all browsers and themes */
    [data-testid="stChatInput"] input,
    [data-testid="stChatInput"] input:focus,
    [data-testid="stChatInput"] input:active,
    .stChatInput input:focus,
    .stChatInput input:active {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        -moz-text-fill-color: #ffffff !important;
        text-shadow: none !important;
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
    }    /* Hide Streamlit elements */
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
    
    /* ULTIMATE OVERRIDE: Force black text for all statistics components */
    /* This targets all possible CSS selectors that could contain statistics */
    .stats-container *, .stats-container, 
    div[class*="stats"] *, div[class*="stats"],
    .stat-value, .stat-label, .stat-item,
    [class*="stat-"] *, [class*="stat-"],
    .stApp .stats-container *,
    html .stats-container *,
    body .stats-container * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        -moz-text-fill-color: #000000 !important;
        text-shadow: none !important;
    }
    
    /* Override for stat labels specifically */
    .stat-label, [class*="stat-label"], 
    .stats-container .stat-label,
    div[class*="stats"] .stat-label {
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
        -moz-text-fill-color: #333333 !important;
    }
    
    /* Browser-specific CSS for text color enforcement */
    @-webkit-keyframes forceBlackText {
        0% { color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
        100% { color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
    }
    
    @-moz-keyframes forceBlackText {
        0% { color: #000000 !important; -moz-text-fill-color: #000000 !important; }
        100% { color: #000000 !important; -moz-text-fill-color: #000000 !important; }
    }
    
    .stat-value {
        -webkit-animation: forceBlackText 0.1s infinite;
        -moz-animation: forceBlackText 0.1s infinite;
    }
    
    /* Force color for markdown content containing statistics */
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] div,
    .stMarkdown strong,
    .stMarkdown span,
    .stMarkdown div {
        color: inherit !important;
    }
    
    /* Override Streamlit's theme-based text colors for main content */
    .stApp[data-theme="dark"] [data-testid="stMain"] *,
    .stApp[data-theme="light"] [data-testid="stMain"] *,
    html[data-theme="dark"] [data-testid="stMain"] *,
    html[data-theme="light"] [data-testid="stMain"] * {
        color: #1a1a1a !important;
    }
    
    .stApp[data-theme="dark"] .stats-container .stat-value,
    .stApp[data-theme="light"] .stats-container .stat-value,
    html[data-theme="dark"] .stats-container .stat-value,
    html[data-theme="light"] .stats-container .stat-value {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        -moz-text-fill-color: #000000 !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
