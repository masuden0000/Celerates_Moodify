# Moodify AI - Music Recommendation System

## 🎵 Overview

Moodify AI adalah aplikasi rekomendasi musik berbasis AI yang menggunakan analisis mood dan natural language processing untuk memberikan rekomendasi musik yang dipersonalisasi. Aplikasi ini menggunakan ChatGPT-style interface untuk interaksi yang natural dan intuitif.

## ✨ Key Features

- **🗣️ ChatGPT-style Interface** - Natural conversation dengan AI agent
- **📝 Chat History Management** - Multiple chat sessions dengan auto-title generation
- **🎵 Music Recommendations** - Berdasarkan mood dan preferensi pengguna
- **🧠 AI-Powered Analysis** - Advanced music feature analysis
- **📱 Responsive Design** - Modern UI dengan dark sidebar theme
- **💾 Export Functionality** - Export chat history ke JSON
- **🔄 Real-time Sync** - Auto-sync chat sessions dan messages

## 🏗️ Architecture

### 📁 Project Structure

```
DSAI_Moodify AI (2)/
├── .streamlit/            # Streamlit configuration
├── .vscode/              # VS Code settings
├── src/                  # Source code organized in modules
│   ├── core/            # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration dan constants
│   │   ├── music_analyzer.py   # Music analysis dan recommendations
│   │   ├── ai_agent.py         # AI agent setup
│   │   ├── utils.py            # Utility functions
│   │   ├── response_cleaner.py # AI response processing
│   │   └── debug_logger.py     # Debug utilities
│   ├── data/            # Data management
│   │   ├── __init__.py
│   │   └── data_manager.py     # Data processing dan loading
│   └── ui/              # User interface components
│       ├── __init__.py
│       ├── styles.py           # CSS styling (ChatGPT-like)
│       ├── ui_components.py    # Statistics display
│       └── sidebar.py          # Chat history sidebar
├── app.py               # Main application file
├── requirements.txt     # Dependencies
├── spotify_data.csv     # Music dataset
└── README.md           # Project documentation
```

### 📝 Module Descriptions

#### `app.py` - Main Application
- Entry point aplikasi Streamlit
- Orchestrates all modules dan components
- Handles main chat flow dan user interactions

#### `src/core/` - Core Business Logic
- **`config.py`** - Application constants dan configuration
- **`music_analyzer.py`** - Music analysis, mood extraction, recommendations
- **`ai_agent.py`** - LangChain AI agent setup dengan Cohere LLM
- **`utils.py`** - Session management, message processing, utilities
- **`response_cleaner.py`** - Clean AI responses dari debug output
- **`debug_logger.py`** - Debugging dan logging utilities

#### `src/data/` - Data Management
- **`data_manager.py`** - Music data loading, processing, dan sample generation

#### `src/ui/` - User Interface
- **`styles.py`** - Modern CSS styling dengan ChatGPT-like sidebar
- **`ui_components.py`** - Statistics dan UI components
- **`sidebar.py`** - Complete chat history management system
## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- pip package manager

### Installation

1. **Clone repository:**
   ```bash
   git clone [repository-url]
   cd "DSAI_Moodify AI (2)"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup API Keys (Optional):**
   - Create `.streamlit/secrets.toml` atau set environment variables
   - Add: `COHERE_API_KEY = "your_api_key_here"`
   - Add: `OPENAI_API_KEY = "your_openai_key_here"` (if using OpenAI)

4. **Run application:**
   ```bash
   streamlit run app.py
   ```

## 🔧 Dependencies

### Core Requirements
```txt
streamlit>=1.28.0          # Web framework
pandas>=2.0.0              # Data manipulation
numpy>=1.24.0              # Numerical operations
```

### AI/ML Libraries
```txt
openai>=1.0.0              # OpenAI integration
langchain>=0.1.0           # LangChain framework
langchain-openai>=0.0.5    # LangChain OpenAI connector
```

### Music Processing
```txt
spotipy>=2.22.1            # Spotify API
librosa>=0.10.0            # Audio analysis
soundfile>=0.12.1          # Audio file handling
```

### Utilities
```txt
requests>=2.31.0           # HTTP requests
python-dotenv>=1.0.0       # Environment variables
python-dateutil>=2.8.0     # Date handling
beautifulsoup4>=4.12.0     # Web scraping
```

## 🎯 Current Features

### 💬 ChatGPT-Style Interface
- **Natural Conversations** - Talk to AI about your music preferences
- **Context Awareness** - AI remembers conversation context
- **Clean Responses** - Advanced response cleaning from debug output

### 📚 Chat History Management
- **Multiple Sessions** - Create dan manage multiple chat sessions
- **Auto-Title Generation** - Chat titles based on first user message
- **Smart Organization** - Sorted by recent activity
- **Export Functionality** - Download chat history as JSON
- **Persistent Storage** - Chat history saved in session state

### 🎵 Music Recommendations
- **Mood-Based Analysis** - Recommendations based on detected mood
- **Audio Feature Analysis** - Valence, energy, danceability analysis
- **Personalized Suggestions** - Tailored to user preferences
- **Real-time Processing** - Instant recommendation generation

### 🎨 Modern UI/UX
- **Dark Sidebar Theme** - ChatGPT-inspired sidebar design
- **Hidden Collapse Button** - Clean interface without distractions
- **Responsive Design** - Works on desktop dan mobile
- **Minimalist Aesthetics** - Clean, modern design language
- **Smooth Interactions** - Seamless user experience

## 📊 Data Processing

### Music Dataset
- **Spotify Features** - Audio features (valence, energy, danceability, etc.)
- **Mood Classification** - Based on valence and energy combinations
- **Fallback Data** - Auto-generated sample data if CSV missing
- **Real-time Analysis** - Dynamic mood detection dari user input

### Chat Data Structure
```json
{
  "chat_sessions": {
    "chat_id": {
      "title": "Auto-generated from first message",
      "messages": [
        {
          "role": "user|bot",
          "content": "message content",
          "timestamp": "ISO datetime"
        }
      ],
      "created_at": "ISO datetime",
      "updated_at": "ISO datetime"
    }
  }
}
```

## 🤖 AI Architecture

### AI Agent System
- **LangChain Integration** - Advanced conversation management
- **Multiple LLM Support** - OpenAI GPT dan Cohere models
- **Tool Integration** - Music analysis, recommendations, web search
- **Memory Management** - Conversation context preservation
- **Response Cleaning** - Automatic debug output removal

### Fallback System
- **Basic Mode** - Rule-based responses when AI unavailable
- **Pattern Matching** - Mood detection via keyword analysis
- **Graceful Degradation** - App works without API keys
- **Error Handling** - User-friendly error messages

## � Recent Updates (v2.0)

### ❌ Removed Features
- **Mood Buttons** - Removed preset mood buttons (Happy, Sad, Chill, Analyze)
- **Quick Actions** - Streamlined to focus on natural conversation
- **Complex UI Elements** - Simplified for better user experience

### ✅ Enhanced Features
- **Improved Chat Flow** - More natural conversation experience
- **Better Error Handling** - Robust datetime serialization for exports  
- **Enhanced Sidebar** - Hidden collapse button, better styling
- **Auto-Title Generation** - Smart chat naming based on content
- **Download Integration** - Direct file download for chat exports

### 🎨 UI/UX Improvements
- **ChatGPT-Style Sidebar** - Dark theme with modern aesthetics
- **Full-Width Buttons** - Better responsive design
- **Clean Interface** - Removed visual clutter
- **Improved Typography** - Better readability
- **Mobile Optimization** - Enhanced mobile experience

## 📈 Analytics & Statistics

### Real-time Tracking
- **Query Processing** - Total user queries processed
- **Recommendation Metrics** - Number of recommendations given
- **Session Management** - Active chat sessions tracking
- **Usage Analytics** - User interaction patterns

### Export Features
- **JSON Export** - Complete chat history dengan metadata
- **Auto-Filename** - Timestamp-based file naming
- **Error Handling** - Robust export functionality
- **Download Integration** - Direct browser download

## 🚨 Troubleshooting

### Common Issues

1. **Chat Export Errors**
   ```
   TypeError: Object of type datetime is not JSON serializable
   ```
   **Solution:** Updated dengan proper datetime serialization

2. **Sidebar Button Styling**
   ```
   Buttons not filling container width
   ```
   **Solution:** Enhanced CSS dengan specific selectors

3. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **AI Features Not Working**
   - Set environment variable `COHERE_API_KEY` atau `OPENAI_API_KEY`
   - Create `.streamlit/secrets.toml` dengan API keys
   - App will fallback to basic mode if AI unavailable

### Performance Optimization
- **Session State Management** - Efficient data persistence
- **Conditional Imports** - Lazy loading for optional dependencies  
- **Caching Strategy** - `@st.cache_data` for data loading
- **Memory Management** - Proper cleanup of large objects

## 📝 Development Guide

### Adding New Features

1. **Identify Module:**
   - Chat functionality → `src/ui/sidebar.py`
   - Music analysis → `src/core/music_analyzer.py`
   - AI features → `src/core/ai_agent.py`
   - UI styling → `src/ui/styles.py`
   - Data processing → `src/data/data_manager.py`

2. **Best Practices:**
   - Follow existing code style dan patterns
   - Add comprehensive docstrings
   - Handle errors gracefully
   - Test dengan dan without optional dependencies
   - Maintain backward compatibility

3. **Testing Strategy:**
   - Test main functionality
   - Test error scenarios  
   - Test responsive design
   - Test export/import functionality

### Code Organization Principles

- **Separation of Concerns** - Clear module responsibilities
- **Modular Design** - Independent, reusable components
- **Error Resilience** - Graceful failure handling
- **User Experience** - Intuitive, responsive interface
- **Scalability** - Easy to extend dan maintain

## 🎯 Roadmap

### Planned Features
- **🎵 Playlist Integration** - Export to Spotify/Apple Music
- **👤 User Profiles** - Save preferences dan history
- **📊 Advanced Analytics** - Detailed usage insights
- **� Social Features** - Share recommendations
- **🎤 Voice Input** - Speech-to-text integration
- **📱 Mobile App** - Native mobile application

### Technical Improvements
- **Database Integration** - Persistent data storage
- **API Optimization** - Faster response times
- **Advanced Caching** - Improved performance
- **Multi-language Support** - Internationalization
- **Real-time Updates** - WebSocket integration

## 📄 License

This project is created for educational purposes as part of the Celerates program.

## 🤝 Contributing

Contributions are welcome! Please follow the development guide dan maintain code quality standards.

## 📞 Support

For questions or issues, please refer to the troubleshooting section atau create an issue in the repository. 
