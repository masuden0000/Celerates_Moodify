"""
AI Agent Controller - Main business logic for Moodify AI
Handles agent setup, mood validation, and AI conversation management
"""

import os
import time

import pandas as pd
import streamlit as st

from src.config.app_config import LLM_AVAILABLE
from src.models.music_analyzer import (
    analyze_mood_features,
    get_enhanced_recommendations,
    search_music_info,
)
from src.services.agent_callback import create_debug_callback
from src.services.debug_logger import (
    debug_logger,
    disable_debug_mode,
    enable_debug_mode,
    log_error,
    log_final_output,
    log_llm_start,
    log_system,
    log_user_input,
)
from src.services.tool_debugger import debug_tool


def validate_and_map_mood(mood_input: str) -> str:
    """Validate and map input mood to valid mood categories"""
    VALID_MOODS = {"happy", "sad", "energy", "calm", "romantic", "neutral"}
    mood_clean = mood_input.lower().strip()

    if mood_clean in VALID_MOODS:
        return mood_clean

    # SPECIAL HANDLING: Check for "musik [mood]" patterns first
    for valid_mood in VALID_MOODS:
        if f"musik {valid_mood}" in mood_clean:
            log_system(
                f"🎯 Mood mapping: '{mood_input}' -> '{valid_mood}' (pattern: 'musik {valid_mood}')"
            )
            return valid_mood
        # Also check for variations like "musik [mood]o" for typos
        if f"musik {valid_mood}o" in mood_clean:
            log_system(
                f"🎯 Mood mapping: '{mood_input}' -> '{valid_mood}' (pattern: 'musik {valid_mood}o')"
            )
            return valid_mood

    MOOD_MAPPING = {
        "makan": "happy",
        "makano": "happy",
        "lapar": "happy",
        "weekend": "happy",
        "libur": "happy",
        "senang": "happy",
        "gembira": "happy",
        "suka": "happy",
        "bahagia": "happy",
        "olahraga": "energy",
        "gym": "energy",
        "workout": "energy",
        "pagi": "energy",
        "semangat": "energy",
        "bangun": "energy",
        "jogging": "energy",
        "run": "energy",
        "jalan": "calm",
        "macet": "calm",
        "kerja": "calm",
        "belajar": "calm",
        "fokus": "calm",
        "santai": "calm",
        "rileks": "calm",
        "tenang": "calm",
        "duduk": "calm",
        "istirahat": "calm",
        "sedih": "sad",
        "sediho": "sad",
        "musik sedih": "sad",
        "musik sediho": "sad",
        "galau": "sad",
        "hujan": "sad",
        "patah hati": "sad",
        "ambyar": "sad",
        "kecewa": "sad",
        "lelah": "sad",
        "cape": "sad",
        "bengong": "sad",
        "pacar": "romantic",
        "kangen": "romantic",
        "cinta": "romantic",
        "rindu": "romantic",
        "sayang": "romantic",
        "valentine": "romantic",
        "rekomendasi": "neutral",
        "saran": "neutral",
        "musik": "neutral",
        "lagu": "neutral",
        "playlist": "neutral",
    }

    for keyword, mapped_mood in MOOD_MAPPING.items():
        if keyword in mood_clean:
            log_system(
                f"🎯 Mood mapping: '{mood_input}' -> '{mapped_mood}' (keyword: '{keyword}')"
            )
            return mapped_mood

    log_system(f"🎯 Mood defaulting to neutral: '{mood_input}' -> 'neutral'")
    return "neutral"


def setup_ai_agent(df: pd.DataFrame):
    """Setup AI agent with tools"""
    if not LLM_AVAILABLE:
        return None

    cohere_api_key = None
    try:
        cohere_api_key = st.secrets.get("COHERE_API_KEY")
    except:
        pass

    if not cohere_api_key:
        cohere_api_key = os.getenv("COHERE_API_KEY")

    if not cohere_api_key:
        st.warning("⚠️ Cohere API Key not found. Running in basic mode.")
        return None

    try:
        from langchain.agents import AgentExecutor, Tool, create_react_agent
        from langchain.memory import ConversationBufferMemory
        from langchain.prompts import PromptTemplate
        from langchain_cohere import ChatCohere
        from pydantic import SecretStr  # Definisikan system prompt

        system_prompt = """
        **IDENTITAS WAJIB - JANGAN PERNAH BERUBAH:**
        Nama kamu: Moodify AI
        Identitas kamu: Moodify AI (BUKAN Coral, BUKAN assistant lain)
        
        **ATURAN IDENTITAS MUTLAK:**
        - JANGAN PERNAH menyebut diri sebagai "Coral" atau nama lain
        - JANGAN PERNAH menyebut diri sebagai "AI assistant chatbot" 
        - SELALU gunakan nama "Moodify AI" atau "Moodify"
        - SELALU gunakan kata ganti "gw" untuk diri sendiri, "lo" untuk user
        
        **RESPONS WAJIB UNTUK PERTANYAAN IDENTITAS:**
        Ketika user bertanya "siapa kamu", "kamu siapa", "who are you", "introduce yourself", atau pertanyaan serupa tentang identitas, WAJIB dan HANYA boleh jawab dengan PERSIS seperti ini:
        
        "Gw adalah Moodify AI, asisten musikmu! 🎵 Gw di sini buat bantu lo nemuin lagu yang pas sama mood dan vibe lo. Mau dengerin musik apa hari ini?"
        
        JANGAN PERNAH jawab dengan respons lain atau menyebut nama selain Moodify AI.
        
        **Persona Utama:**
        Kamu adalah Moodify AI, asisten musik yang paling ngertiin selera musik Gen Z. Kamu itu asek, santai, dan passion-nya soal musik gak ada abisnya. Anggep aja kamu itu temen yang selalu punya playlist pas buat segala situasi.
        
        - **Nama:** Moodify AI (atau panggil aja Moodify) - JANGAN PERNAH sebut nama lain
        - **Identitas:** Gw adalah Moodify AI, asisten musikmu yang siap bantu lo nemuin lagu yang pas buat mood lo!
        - **Gaya Bahasa:** Bahasa yang digunakan bahasa indonesia. Pake bahasa gaul Jakarta (gw, lo, anjir, gokil, vibe, dll). Santai, to the point, dan gak kaku.
        - **Karakter:**
            - **Music Nerd:** Tau banget soal musik, dari yang lagi trending sampe hidden gems.
            - **Empatetik:** Bisa nangkep mood user, bahkan yang gak diomongin langsung.
            - **Proaktif & Interaktif:** Suka nanya balik buat mastiin rekomendasinya pas.
            - **Humoris:** Lemparkan humor cerdas atau referensi pop culture kalo pas.
            - **Visual:** Gunakan emoji yang relevan secara natural (🎶🔥🎧✨😌🕺💃).
            - **Smart Responder:** Kalau ada tool yang butuh konfirmasi (seperti typo correction), langsung kasih respons yang meminta konfirmasi ke user dengan jelas dan friendly.
          
        **Tugas Inti:**
        1.  **Deteksi & Klasifikasi Vibe:** Tugas PERTAMA dan UTAMA adalah menganalisis input user (eksplisit & implisit) dan WAJIB mengklasifikasikannya menjadi **SATU** dari mood berikut: `happy`, `sad`, `energy`, `calm`, `romantic`, `neutral`.
        2.  **Rekomendasi Cerdas:** Setelah mood terdeteksi, gunakan tool yang sesuai untuk memberikan rekomendasi lagu yang cocok. Selalu kasih alasan singkat kenapa lo merekomendasikan itu.
        3.  **Analisis Musik:** Jelasin karakteristik lagu (beat, lirik, genre, instrumen) pake bahasa yang gampang dimengerti.
        4.  **Musicopedia:** Jadi ensiklopedia musik berjalan buat cari info soal artis, band, lagu, atau sejarah musik.
        5.  **Playlist Kurator:** Buatin playlist simpel (3-5 lagu) berdasarkan tema dari user.
        6.  **Pencarian Lirik:** Cari lirik lagu dengan koreksi AI otomatis untuk typo dan web search multi-source.
        7.  **Smart Follow-up:** Kalau tool memberikan respons yang butuh konfirmasi (seperti typo correction), JANGAN tampilkan thought process, tapi langsung berikan respons yang ramah dan jelas meminta konfirmasi.
        
        ---
        
        **INTELLIGENT RESPONSE STRATEGY:**
        
        PENTING: Kalau kamu menggunakan tool dan hasilnya adalah pertanyaan konfirmasi (seperti "Apakah yang kamu maksudkan adalah...?"), jangan tampilkan thought process. Langsung berikan respons final yang:
        1. Mengakui ada kemungkinan typo/kesalahan
        2. Menawarkan koreksi dengan bahasa yang friendly
        3. Meminta konfirmasi dengan jelas
        4. Memberikan alternatif jika user tidak setuju
        
        **Contoh Smart Response:**
        Tool Output: "Hmm, sepertinya ada typo nih. Apakah yang kamu maksudkan adalah **Right Now - One Direction**? Ketik 'ya' untuk konfirmasi..."
        
        Your Final Answer: "Eh, kayaknya ada typo dikit nih di nama lagunya 😅 Lo maksudnya **'Right Now - One Direction'** kah? Kalau iya, ketik 'ya' aja buat gw cariin liriknya. Kalau bukan, coba ketik ulang ya dengan ejaan yang lebih jelas! 🎵"
        
        ---
        
        **LOGIKA DETEKSI MOOD & KLASIFIKASI (WAJIB DIIKUTI)**
        
        Sebelum melakukan apapun, tugas pertamamu adalah menerjemahkan input user menjadi **SATU** dari enam mood berikut: `happy`, `sad`, `energy`, `calm`, `romantic`, `neutral`. 
        
        **PENTING:** Kamu HARUS menggunakan salah satu dari 6 mood ini saja, JANGAN menggunakan kata lain seperti "makan", "olahraga", "kerja", dll. Gunakan mood mapping yang benar:
        
        **2. Tabel Referensi Mood Mapping:**
        | Aktivitas/Situasi User | Mood yang BENAR |
        | :--- | :--- |
        | "mau makan", "lapar", "makanan" | `happy` |
        | "abis olahraga", "gym", "workout" | `energy` |
        | "lagi di jalan", "macet", "kerja", "belajar" | `calm` |
        | "hujan", "galau", "sedih" | `sad` |
        | "mikirin dia", "kangen", "romantic" | `romantic` |
        | "rekomendasi lagu", "musik apa" | `neutral` |
        
        **WAJIB:** Sebelum memanggil tool, pastikan input mood hanya salah satu dari: happy, sad, energy, calm, romantic, neutral
        
        ---
        
        **CARA MENGGUNAKAN TOOLS (SANGAT PENTING!):**
        
        Kamu memiliki 4 tools yang bisa digunakan:
        1. **recommend_songs** - untuk memberikan rekomendasi lagu berdasarkan mood
        2. **analyze_features** - untuk menganalisis fitur musik 
        3. **search_info** - untuk mencari informasi tentang musik/artis
        4. **search_lyrics** - untuk mencari lirik lagu dengan AI correction
        
        **ATURAN PEMANGGILAN TOOL:**
        - SELALU gunakan format: Action: [nama_tool]
        - SELALU gunakan format: Action Input: [mood_yang_valid_saja]
        - JANGAN PERNAH gunakan format: Action: recommend_songs(mood="sad")
        - GUNAKAN format yang BENAR: Action: recommend_songs, Action Input: happy
        
        **CONTOH PEMANGGILAN YANG BENAR:**
        
        User: "mau makan nih, dengerin lagu apa?"
        
        Thought: User mau makan, ini adalah aktivitas yang menyenangkan, jadi mood-nya "happy"
        Action: recommend_songs
        Action Input: happy
        Observation: [hasil dari tool]
        Final Answer: Wah, lagi mau makan nih! Perfect timing buat lagu yang happy... [response]
        
        **CONTOH PEMANGGILAN YANG SALAH (JANGAN DIGUNAKAN!):**
        Action: recommend_songs(mood="makan") ❌
        Action Input: makan ❌
        Action Input: makano ❌
        """  # LLM dengan system prompt terintegrasi
        llm = ChatCohere(
            model="command-r-plus",
            temperature=0.3,
            cohere_api_key=SecretStr(cohere_api_key) if cohere_api_key else None,
            verbose=False,
        )

        # Inject system prompt ke dalam LLM
        llm.bind(system=system_prompt)

        # Define tools dengan deskripsi yang lebih baik dan debugging        @debug_tool("recommend_songs")
        def recommend_songs(mood: str) -> str:
            """Recommend songs with proper formatting and error handling"""
            try:
                validated_mood = validate_and_map_mood(mood)
                log_system(f"🎯 Mood validation: '{mood}' -> '{validated_mood}'")

                result = get_enhanced_recommendations(df, validated_mood, 5)

                if not result or "tidak ada lagu" in result.lower():
                    return f"Waduh, gak ada lagu yang cocok untuk mood '{validated_mood}' nih 😅 Coba mood yang lain ya!"

                return result.strip()

            except Exception as e:
                log_error(e, f"Error in recommend_songs with input: {mood}")
                return f"Maaf, ada error saat cari lagu: {str(e)} 😅"

        @debug_tool("analyze_features")
        def analyze_features(mood: str) -> str:
            """Analyze music features based on mood"""
            try:
                validated_mood = validate_and_map_mood(mood)
                log_system(
                    f"🎯 Analyze mood validation: '{mood}' -> '{validated_mood}'"
                )

                analysis_result = analyze_mood_features(df, validated_mood)
                return analysis_result.strip()

            except Exception as e:
                log_error(e, f"Error in analyze_features with input: {mood}")
                return f"Maaf, ada error saat analisis musik: {str(e)} 😅"

        @debug_tool("search_info")
        def search_info(query: str) -> str:
            """Search for music, artist, or band information"""
            return search_music_info(query)

        @debug_tool("search_lyrics")
        def search_lyrics(query: str) -> str:
            """Cari lirik lagu dengan Gemini AI correction dan web search"""
            try:
                from src.services.lyrics_service import (
                    extract_song_from_query,
                    search_lyrics_with_gemini,
                )

                # Extract song info from query
                song_query = extract_song_from_query(query)

                # Search with Gemini AI
                result = search_lyrics_with_gemini(song_query)

                # Return result directly tanpa additional processing
                return result

            except ImportError:
                return "❌ Fitur pencarian lirik belum tersedia. Install google-generativeai dengan: pip install google-generativeai"
            except Exception as e:
                log_error(e, f"Error in search_lyrics with query: {query}")
                return f"❌ Maaf, ada error saat mencari lirik: {str(e)}"

        tools = [
            Tool(
                name="recommend_songs",
                func=recommend_songs,
                description="""
                        WAJIB DIGUNAKAN ketika user meminta rekomendasi musik/lagu dalam bentuk apapun.
                        PENTING: Input harus salah satu dari mood yang valid: happy, sad, energy, calm, romantic, neutral
                        Jangan gunakan kata lain seperti "makan", "olahraga", "kerja" - gunakan mood mapping yang benar.
                        Keywords trigger: 'rekomendasi', 'rekomen', 'saranin', 'kasih tau lagu', 'mood', 'lagu buat', 'musik untuk'.
                        
                        Contoh penggunaan yang BENAR:
                        - User: "mau makan nih" -> Input: happy (karena makan = aktivitas menyenangkan)
                        - User: "abis olahraga" -> Input: energy (karena butuh semangat)
                        - User: "lagi galau" -> Input: sad (mood negatif)
                        
                        Input: HANYA salah satu dari: happy, sad, energy, calm, romantic, neutral
                        Output: Daftar rekomendasi lagu yang sudah diformat dengan penjelasan.
                        """,
            ),
            Tool(
                name="analyze_features",
                func=analyze_features,
                description="""
                        WAJIB DIGUNAKAN ketika user meminta ANALISIS karakteristik musik berdasarkan mood.
                        Keywords trigger: 'analisis', 'analyze', 'karakteristik', 'fitur musik', 'ciri-ciri musik'.
                        
                        Contoh penggunaan:
                        - User: "analyze music dengan mood sad" -> Input: sad
                        - User: "analisis karakteristik musik sedih" -> Input: sad
                        - User: "bagaimana ciri musik happy" -> Input: happy
                        
                        PENTING: Input harus salah satu dari mood yang valid: happy, sad, energy, calm, romantic, neutral
                        Tool ini akan memberikan analisis statistik dan karakteristik audio dari musik dengan mood tertentu.
                        
                        Input: HANYA salah satu dari: happy, sad, energy, calm, romantic, neutral
                        Output: Analisis karakteristik musik yang sudah diformat dengan statistik dan contoh lagu.
                        """,
            ),
            Tool(
                name="search_info",
                func=search_info,
                description="Berguna untuk mencari INFORMASI FAKTUAL dan data spesifik tentang dunia musik.",
            ),
            Tool(
                name="search_lyrics",
                func=search_lyrics,
                description="""
                        WAJIB DIGUNAKAN ketika user meminta lirik lagu atau kata-kata lagu.
                        Tool ini menggunakan Gemini AI untuk koreksi typo otomatis dan pencarian lirik langsung.
                        
                        Keywords trigger: 'lirik', 'lyrics', 'kata-kata lagu', 'syair', 'teks lagu', 'chord'.
                        
                        Contoh penggunaan:
                        - User: "lirik right no one direction" -> Input: "right no one direction"
                        - User: "cari lirik bohemian rapsody" -> Input: "bohemian rapsody" 
                        - User: "kata-kata lagu shape of you" -> Input: "shape of you"
                        
                        Fitur khusus:
                        - Otomatis koreksi typo menggunakan Gemini AI
                        - Langsung berikan lirik tanpa konfirmasi tambahan
                        - Output berformat rapi dengan judul, artis, dan lirik
                        - Fallback ke web search jika Gemini tidak tersedia
                        
                        PENTING: SELALU berikan hasil pencarian langsung ke user, jangan minta konfirmasi.
                        Input: Query pencarian lirik (judul lagu, artis, atau kombinasi)
                        Output: Lirik lagu dengan format yang rapi
                        """,
            ),
        ]

        memory = ConversationBufferMemory()
        memory_key = ("chat_history",)
        return_messages = (
            False  # Custom prompt template dengan format yang lebih eksplisit
        )
        custom_prompt_text = f"""You are Moodify AI, a music assistant. NEVER introduce yourself as "Coral" or any other name.

IDENTITY RULES:
- Your name is ONLY "Moodify AI" 
- When asked "siapa kamu" or "who are you", respond EXACTLY: "Gw adalah Moodify AI, asisten musikmu! 🎵 Gw di sini buat bantu lo nemuin lagu yang pas sama mood dan vibe lo. Mau dengerin musik apa hari ini?"
- Use Indonesian slang: "gw" for yourself, "lo" for user
- NEVER say you are "Coral" or "AI assistant chatbot"

{system_prompt}

Answer the following questions as best you can. You have access to the following tools:

{{tools}}

CRITICAL TOOL CALLING FORMAT - MUST FOLLOW EXACTLY:

✅ CORRECT FORMAT:
Action: recommend_songs
Action Input: happy

Action: analyze_features  
Action Input: sad

❌ WRONG FORMAT (NEVER USE):
Action: recommend_songs(mood="happy")
Action: analyze_features("musik sedih")
Action Input: mood="happy"
Action Input: musik sedih
Action Input: musik sediho

MOOD VALIDATION - ONLY USE THESE MOODS:
Valid moods: happy, sad, energy, calm, romantic, neutral

MOOD MAPPING EXAMPLES:
- "mau makan" -> use "happy" (not "makan")
- "abis olahraga" -> use "energy" (not "olahraga") 
- "lagi galau" -> use "sad" (not "galau")
- "musik sedih" -> use "sad" (not "musik sedih")
- "analyze sad music" -> use "sad" (not "musik sedih")

SPECIAL INSTRUCTIONS FOR ANALYZE_FEATURES TOOL:
- When user asks for analysis of music characteristics, use analyze_features
- Input must be a valid mood only (happy, sad, energy, calm, romantic, neutral)
- Do NOT add extra interpretation - return the tool output directly
- Tool output is already formatted and complete

SPECIAL INSTRUCTIONS FOR SEARCH_LYRICS TOOL:
- When user asks for lyrics, use search_lyrics
- Input should be the song title and artist name
- ALWAYS return the tool result EXACTLY as provided - do NOT modify or expand
- Do NOT add additional lyrics content beyond what the tool returns
- The tool already provides complete formatted response

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do and map the situation to a valid mood
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action (must be a valid mood: happy, sad, energy, calm, romantic, neutral)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{input}}
Thought:{{agent_scratchpad}}"""

        prompt = PromptTemplate.from_template(custom_prompt_text)

        # Create the react agent dengan prompt custom
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

        # Create agent executor dengan memory
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,  # Handle parsing errors gracefully
            max_iterations=5,  # Limit iterations to prevent loops
            return_intermediate_steps=True,
        )

        log_system("AI Agent berhasil diinisialisasi dengan mood validation")
        return agent_executor

    except Exception as e:
        st.error(f"Error setting up AI agent: {str(e)}")
        log_error(e, "Error during agent setup")
        return None


# =============================================================================
# DEBUG AGENT RUNNER
# =============================================================================


def run_agent_with_debug(agent, user_input: str, enable_debug: bool = True):
    """
    Menjalankan agent dengan debug logging

    Args:
        agent: LangChain agent instance
        user_input: Input dari user
        enable_debug: Whether to enable debug mode

    Returns:
        str: Response dari agent
    """
    if not agent:
        return "⚠️ Agent tidak tersedia. Pastikan API key sudah dikonfigurasi."

    # Enable/disable debug mode
    if enable_debug:
        enable_debug_mode()
    else:
        disable_debug_mode()

    # Log user input
    log_user_input(user_input)

    # Start timing
    start_time = time.time()

    try:
        # Log start of processing
        log_system("Memulai pemrosesan dengan AI Agent")

        # Run the agent executor
        result = agent.invoke(
            {
                "input": user_input,
                "chat_history": st.session_state.get("chat_history", ""),
            }
        )

        # Extract response from result
        response = (
            result.get("output", str(result))
            if isinstance(result, dict)
            else str(result)
        )

        # Calculate total duration
        total_duration = time.time() - start_time

        # Log final output
        log_final_output(response, total_duration)

        return response

    except Exception as e:
        log_error(e, "Error during agent execution")
        return f"❌ Terjadi error: {str(e)}"


def update_agent_memory_with_streamlit_history(agent):
    if not agent or not hasattr(agent, "memory"):
        return
    messages = st.session_state.get("messages", [])
    history = ""
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        history += f"{role}: {content}\\n"
    agent.memory.chat_memory.clear()
    agent.memory.chat_memory.add_user_message(history)


def toggle_debug_mode():
    """Toggle debug mode on/off"""
    if debug_logger.enable_terminal_output:
        disable_debug_mode()
        return "🔧 Debug mode DISABLED"
    else:
        enable_debug_mode()
        return "🔧 Debug mode ENABLED"


def get_debug_summary():
    """Get debug session summary"""
    debug_logger.print_summary()
    return "📊 Debug summary printed to console"


def clear_debug_logs():
    """Clear all debug logs"""
    debug_logger.clear_logs()
    return "🧹 Debug logs cleared"
