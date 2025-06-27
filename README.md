# 🎵 Moodify AI - Music Recommendation System

Aplikasi rekomendasi musik berbasis AI yang menggunakan **Cohere LLM** untuk analisis mood dan memberikan rekomendasi musik yang dipersonalisasi melalui interface ChatGPT-style.

## ✨ Key Features

- **🤖 Cohere AI** - Powered by Cohere's advanced language model
- **🗣️ ChatGPT-style Interface** - Natural conversation dengan AI agent
- **📝 Chat History Management** - Multiple chat sessions dengan auto-title generation
- **🎵 Smart Music Recommendations** - Berdasarkan mood dan preferensi pengguna
- **🧠 Advanced Analysis** - Music feature analysis dengan ML
- **📱 Responsive Design** - Modern UI dengan dark sidebar theme
- **💾 Export Functionality** - Export chat history ke JSON
- **🔄 Real-time Sync** - Auto-sync chat sessions dan messages
- **📊 Data Visualization** - Interactive charts dengan Plotly
- **🔍 Web Search** - Real-time music info via Google Search

## � Quick Start

### Prerequisites

- Python 3.11 (recommended) atau 3.12
- Git dengan Git LFS support
- Cohere API Key (dari cohere.ai)

### Installation

1. **Clone repository:**
   ```bash
   git clone https://github.com/masuden0000/Celerates_Moodify.git
   cd Celerates_Moodify
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   py -3.11 -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Cohere API:**
   - Kunjungi [Cohere Dashboard](https://cohere.ai/)
   - Buat account dan generate API key
   - Buat file `.streamlit/secrets.toml`:
   ```toml
   [cohere]
   api_key = "your_cohere_api_key_here"
   ```

5. **Download data (Git LFS):**
   ```bash
   git lfs pull
   ```

6. **Run the application:**
   ```bash
   streamlit run app.py
   ```

7. **Open browser:**
   - Local: http://localhost:8501
   - Network: akan ditampilkan di terminal

## 🎯 How to Use

1. **Start conversation** - Ketik mood atau preferensi musik Anda
2. **Get recommendations** - AI akan analisis dan berikan rekomendasi
3. **Explore data** - Lihat visualisasi dan statistik musik
4. **Multiple chats** - Kelola berbagai sesi percakapan
5. **Export history** - Download riwayat chat dalam format JSON

### Example Prompts:
- "Lagi sedih nih, kasih lagu yang cocok"
- "Mau workout, recommend lagu energik"
- "Analisis musik happy dong"
- "Siapa itu Taylor Swift?"
- "Lagu indie rock yang bagus apa?"

## 🏗️ Architecture

### 📁 Project Structure

```
DSAI_Moodify AI (2)/
├── .streamlit/
│   ├── config.toml         # Streamlit configuration
│   └── secrets.toml        # API keys (tidak di-commit)
├── src/
│   ├── core/
│   │   ├── ai_agent.py           # Google Gemini setup
│   │   ├── music_analyzer.py     # Music analysis
│   │   ├── utils.py              # Utility functions
│   │   └── config.py             # Configuration
│   ├── data/
│   │   ├── data_manager.py       # Data processing
│   │   └── lfs_handler.py        # Git LFS support
│   └── ui/
│       ├── sidebar.py            # Chat management
│       ├── styles.py             # CSS styling
│       └── ui_components.py      # UI components
├── app.py                  # Main application
├── requirements.txt        # Dependencies
├── packages.txt           # System dependencies
├── spotify_data.csv       # Music dataset (via Git LFS)
└── README.md             # This file
```
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

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. **Fork/Push ke GitHub**
2. **Kunjungi** [share.streamlit.io](https://share.streamlit.io)
3. **Connect GitHub** account
4. **Deploy** repository: `masuden0000/Celerates_Moodify`
5. **Add secrets** di Streamlit Cloud dashboard:
   ```
   [google]
   api_key = "your_google_gemini_api_key"
   ```

### Local Development Server

```bash
# Production mode
streamlit run app.py --server.port 8501

# Development mode dengan auto-reload
streamlit run app.py --server.runOnSave true
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Version Error
```
TypeError: typevar() got an unexpected keyword argument 'default'
```
**Solution:** Gunakan Python 3.11 atau 3.12, bukan 3.13
```bash
py -3.11 -m venv venv
```

#### 2. Git LFS File Not Found
```
spotify_data.csv not found!
```
**Solution:** Pull LFS files
```bash
git lfs pull
```

#### 3. Google API Key Error
```
API key tidak valid
```
**Solution:** 
- Periksa API key di `.streamlit/secrets.toml`
- Pastikan API key dari [Google AI Studio](https://makersuite.google.com/app/apikey)

#### 4. Package Installation Error
**Solution:** Upgrade pip dan install ulang
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Streamlit App Tidak Load
**Solution:** Clear cache
```bash
streamlit cache clear
```

### Performance Tips

- **Memory**: Dataset besar, gunakan `@st.cache_data`
- **Loading**: Tunggu "Data loaded successfully!" sebelum interact
- **Browser**: Gunakan Chrome/Firefox untuk performa terbaik
- **Internet**: Butuh koneksi untuk Google Gemini API

## 🤝 Contributing

1. **Fork** repository
2. **Create feature branch:** `git checkout -b feature/AmazingFeature`
3. **Commit changes:** `git commit -m 'Add AmazingFeature'`
4. **Push to branch:** `git push origin feature/AmazingFeature`
5. **Open Pull Request**

## 📄 License

Distributed under MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- **Google Gemini** - Free AI API
- **Streamlit** - Web app framework
- **Spotify** - Music dataset
- **Plotly** - Interactive visualizations
- **Langchain** - AI orchestration

## 📞 Contact

- **Author:** Huda Rasyad Wicaksono
- **Project:** [Celerates_Moodify](https://github.com/masuden0000/Celerates_Moodify)
- **Streamlit App:** [Deploy Link Here]

---

**⭐ Star this repo if you find it helpful!**
