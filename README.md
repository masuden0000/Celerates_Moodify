# Moodify AI - Music Recommendation System

## Struktur Proyek

Proyek ini telah dirapihkan dengan memisahkan kode ke dalam beberapa file untuk meningkatkan maintainability dan keterbacaan:

### 📁 File Structure

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
│   │   └── utils.py            # Utility functions
│   ├── data/            # Data management
│   │   ├── __init__.py
│   │   └── data_manager.py     # Data processing dan loading
│   └── ui/              # User interface components
│       ├── __init__.py
│       ├── styles.py           # CSS styling
│       └── ui_components.py    # UI components
├── app.py               # Main application file
├── requirements.txt     # Dependencies
├── spotify_data.csv     # Music dataset
└── README.md           # Project documentation
```

### 📝 Deskripsi File

#### `app.py` - Main Application

- Entry point aplikasi
- Setup konfigurasi Streamlit
- Mengelola flow utama aplikasi
- Import dan orchestrate semua modules

#### `src/core/` - Core Business Logic

- **`config.py`** - Konstanta MOOD_KEYWORDS, MOOD_EMOJIS, GENRE_EMOJIS dan import dependencies
- **`music_analyzer.py`** - Ekstraksi mood, algoritma rekomendasi, analisis fitur musik
- **`ai_agent.py`** - Setup LangChain AI agent, konfigurasi Cohere LLM
- **`utils.py`** - Session state management, response handling, helper functions

#### `src/data/` - Data Management

- **`data_manager.py`** - Loading data musik, sample data generation, data processing

#### `src/ui/` - User Interface

- **`styles.py`** - CSS styling untuk UI minimalis dan responsive design
- **`ui_components.py`** - Render song cards, mood buttons, statistics display

## 🚀 Cara Menjalankan

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan aplikasi:**

   ```bash
   streamlit run app.py
   ```

3. **Optional - Setup API Key:**
   - Buat file `.streamlit/secrets.toml` atau set environment variable
   - Tambahkan `COHERE_API_KEY = "your_api_key_here"`

## 🔧 Dependencies

- `streamlit` - Web framework
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `plotly` - Visualization (optional)
- `langchain_cohere` - AI agent (optional)
- `duckduckgo_search` - Web search (optional)

## 🎯 Fitur

- **Music Recommendations** - Berdasarkan mood dan preferensi
- **Mood Detection** - Dari input text pengguna
- **Music Analysis** - Analisis fitur audio berdasarkan mood
- **AI Chat** - Conversational interface dengan AI agent
- **Web Search** - Pencarian informasi musik online
- **Responsive UI** - Design minimalis dan mobile-friendly

## 📊 Data

- Dataset musik dengan fitur audio (valence, energy, danceability, dll.)
- Jika `spotify_data.csv` tidak ada, sistem akan generate sample data
- Klasifikasi mood berdasarkan kombinasi valence dan energy

## 🤖 AI Features

- **Basic Mode** - Pattern matching dan rule-based responses
- **AI Mode** - LangChain agent dengan Cohere LLM
- **Tools** - Song recommendation, feature analysis, web search
- **Memory** - Conversation history management

## 🎨 UI/UX

- **Minimalist Design** - Clean dan modern interface
- **Chat Interface** - Natural conversation flow
- **Quick Actions** - Mood selection buttons
- **Statistics** - Real-time usage analytics
- **Responsive** - Mobile-friendly design

## 📈 Analytics

- Total queries processed
- Recommendations given
- User interaction tracking
- Session state management

## 🔧 Development Notes

### Code Organization Benefits

- **Maintainability**: Kode lebih mudah dipelihara dan dikembangkan
- **Reusability**: Komponen dapat digunakan kembali di bagian lain
- **Testing**: Setiap modul dapat ditest secara terpisah
- **Collaboration**: Tim dapat bekerja pada file yang berbeda
- **Modularity**: Perubahan pada satu bagian tidak mempengaruhi yang lain
- **Scalability**: Mudah menambahkan fitur baru dengan folder terorganisir
- **Separation of Concerns**: UI, business logic, dan data terpisah dengan jelas

### Import Dependencies

Beberapa modul memiliki import yang conditional:

- `duckduckgo_search` - Untuk web search functionality
- `langchain_cohere` - Untuk AI agent features
- `plotly` - Untuk visualisasi (belum diimplementasi)

### Error Handling

- Graceful fallback jika dependencies tidak tersedia
- Basic mode sebagai backup untuk AI features
- User-friendly error messages

## 🚨 Troubleshooting

### Common Issues

1. **ImportError untuk optional dependencies**

   ```bash
   pip install duckduckgo-search langchain-cohere
   ```

2. **Streamlit tidak bisa load custom CSS**

   - Pastikan `src/ui/styles.py` ada dan dapat diakses
   - Check import path di `app.py`

3. **Data tidak ter-load**

   - Sistem akan otomatis generate sample data
   - CSV file optional, bisa menggunakan data dummy

4. **AI features tidak berfungsi**
   - Set environment variable `COHERE_API_KEY`
   - Atau buat file `.streamlit/secrets.toml`

### Performance Tips

- `@st.cache_data` untuk caching data loading
- Session state untuk persistence
- Lazy loading untuk optional dependencies

## 📝 Contributing

Untuk menambahkan fitur baru:

1. **Identifikasi modul yang tepat**

   - UI changes → `src/ui/ui_components.py` atau `src/ui/styles.py`
   - Data processing → `src/data/data_manager.py`
   - Music logic → `src/core/music_analyzer.py`
   - AI features → `src/core/ai_agent.py`
   - Utility functions → `src/core/utils.py`
   - Configuration → `src/core/config.py`

2. **Maintain consistency**

   - Follow existing code style
   - Add docstrings untuk functions
   - Handle errors gracefully

3. **Test changes**
   - Run aplikasi setelah changes
   - Test dengan dan tanpa optional dependencies
   - Verify responsive design

## 🎯 Future Enhancements

- **Visualization**: Integrasi dengan plotly untuk charts
- **User Profiles**: Simpan preferensi pengguna
- **Playlist Export**: Export ke Spotify/Apple Music
- **Social Features**: Share recommendations
- **Advanced Analytics**: User behavior tracking

## 🏗️ Folder Organization

### Prinsip Organisasi

Proyek ini menggunakan prinsip **Separation of Concerns** dengan pembagian folder sebagai berikut:

- **`src/core/`** - Business logic dan core functionality
- **`src/data/`** - Data management dan processing
- **`src/ui/`** - User interface dan presentation layer

### Import Hierarchy

```python
# Main app imports from organized modules
from src.ui.styles import load_custom_css
from src.data.data_manager import load_music_data
from src.core.ai_agent import setup_ai_agent
```

### Benefits of This Structure

1. **Clear Responsibility** - Setiap folder memiliki tanggung jawab yang jelas
2. **Easy Navigation** - Developer mudah menemukan file yang dibutuhkan
3. **Scalable Architecture** - Mudah menambahkan modul baru
4. **Professional Structure** - Mengikuti best practices software development
# Celerates_Moodify
# Celerates_Moodify 
"# Celerates_Moodify" 
"# Celerates_Moodify" 
"# Celerates_Moodify" 
# Celerates_Moodify
# Celerates_Moodify 
