import os

import pandas as pd
import streamlit as st

from src.core.config import LLM_AVAILABLE
from src.core.music_analyzer import (
    analyze_mood_features,
    get_song_recommendations,
    search_music_info,
)

# =============================================================================
# AI AGENT SETUP
# =============================================================================


def setup_ai_agent(df: pd.DataFrame):
    """Setup AI agent with tools"""
    if not LLM_AVAILABLE:
        return None

    cohere_api_key = st.secrets.get("COHERE_API_KEY") or os.getenv("COHERE_API_KEY")

    if not cohere_api_key:
        st.warning("⚠️ Cohere API Key not found. Running in basic mode.")
        return None

    try:
        from langchain.agents import AgentType, Tool, initialize_agent
        from langchain.memory import ConversationBufferMemory
        from langchain_cohere import ChatCohere

        # LLM dengan system prompt yang baik
        llm = ChatCohere(
            model="command-r-plus",
            temperature=0.3,
            cohere_api_key=cohere_api_key,  # type: ignore
        )

        # Set system prompt untuk LLM
        system_prompt = """
        Kamu adalah AI Assistant khusus musik bernama Moodify. Gunakan bahasa Indonesia yang santai dan friendly.
        
        KEPRIBADIAN:
        - Berbicara dengan gaya anak muda Indonesia yang akrab
        - Gunakan emoji yang relevan untuk musik 🎵🎤🎧
        - Selalu antusias tentang musik
        - Ramah dan interaktif
        
        TUGAS UTAMA:
        1. Mengenali mood dari input user (bahkan yang tersirat)
        2. Memberikan rekomendasi musik sesuai mood
        3. Menganalisis karakteristik musik 
        4. Mencari informasi tentang artis/band/lagu
        
        CARA MENGENALI MOOD TERSIRAT:
        - "mau makan pagi/sarapan" = happy (aktivitas positif pagi)
        - "bosan nih" = neutral/sad
        - "workout/gym/olahraga" = energetic/happy
        - "galau/sedih" = sad
        - "party/main/hangout" = happy
        - "santai/relax" = neutral
        - "capek/lelah" = sad/neutral
        - "weekend/liburan" = happy
        - "kerja/belajar" = neutral
        
        BATASAN PENTING:
        - Jika user bertanya di luar konteks musik, jawab: "Sorry bro, gw agent khusus musik nih! 🎵 Tanya aja yang berhubungan sama lagu, artis, atau mood musik ya!"
        - Fokus HANYA pada: musik, lagu, artis, band, mood musik, genre, instrumen
        
        CONTOH RESPON:
        - Input: "Lagi mau sarapan nih" → Deteksi mood: happy → Kasih rekomendasi upbeat
        - Input: "Siapa itu One Direction?" → Cari info tentang band tersebut
        - Input: "Lagi galau" → Deteksi mood: sad → Kasih rekomendasi sad songs
        
        Selalu gunakan tools yang tersedia untuk memberikan informasi akurat!
        """

        # Define tools dengan deskripsi yang lebih baik
        def recommend_songs(mood: str) -> str:
            """Rekomendasikan lagu berdasarkan mood"""
            recommendations = get_song_recommendations(df, mood, 5)
            if not recommendations:
                return f"Tidak ditemukan lagu untuk mood '{mood}'. Coba mood lain seperti 'happy', 'sad', atau 'neutral'."

            output = f"🎵 **Rekomendasi Lagu untuk Mood '{mood.upper()}':**\n\n"
            for i, song in enumerate(recommendations, 1):
                output += f"{i}. **{song['track_name']}**\n"
                output += f"   🎤 {song['artist_name']} • {song['genre']}\n"
                output += f"   ⭐ Popularitas: {song['popularity']}/100\n\n"

            output += "🎧 Selamat menikmati musik sesuai mood kamu!"
            return output

        def analyze_features(mood: str) -> str:
            """Analisis fitur musik berdasarkan mood"""
            analysis_result = analyze_mood_features(df, mood)
            return f"ANALYSIS_OUTPUT_START\n{analysis_result}\nANALYSIS_OUTPUT_END\n\nAnalisis musik di atas menunjukkan karakteristik khas dari mood '{mood}'."

        def search_info(query: str) -> str:
            """Cari informasi tentang musik, artis, atau band"""
            return search_music_info(query)

        tools = [
            Tool(
                name="recommend_songs",
                func=recommend_songs,
                description="Rekomendasikan lagu berdasarkan mood pengguna. Gunakan ini ketika user meminta rekomendasi musik atau menyebutkan mood/aktivitas tertentu.",
            ),
            Tool(
                name="analyze_features",
                func=analyze_features,
                description="Analisis fitur audio musik berdasarkan mood. Gunakan ini ketika user ingin tahu karakteristik musik dari mood tertentu.",
            ),
            Tool(
                name="search_info",
                func=search_info,
                description="Cari informasi tentang artis, band, lagu, atau topik musik lainnya. Gunakan ini ketika user bertanya tentang informasi musik spesifik.",
            ),
        ]

        # System prompt yang lebih baik
        system_prompt = """
        Kamu adalah AI Assistant khusus musik bernama Moodify. Gunakan bahasa Indonesia yang santai dan friendly.
        
        KEPRIBADIAN:
        - Berbicara dengan gaya anak muda Indonesia yang akrab
        - Gunakan emoji yang relevan untuk musik 🎵🎤🎧
        - Selalu antusias tentang musik
        - Ramah dan interaktif
        
        TUGAS UTAMA:
        1. Mengenali mood dari input user (bahkan yang tersirat)
        2. Memberikan rekomendasi musik sesuai mood
        3. Menganalisis karakteristik musik 
        4. Mencari informasi tentang artis/band/lagu
        
        CARA MENGENALI MOOD:
        - "mau makan pagi" = happy (aktivitas positif)
        - "bosan nih" = neutral/sad
        - "workout" = energetic/happy
        - "galau" = sad
        - "party" = happy
        - "santai" = neutral
        
        BATASAN:
        - Jika user bertanya di luar konteks musik, jawab: "Sorry bro, gw agent khusus musik nih! Tanya aja yang berhubungan sama lagu, artis, atau mood musik ya 🎵"
        - Fokus hanya pada topik musik, lagu, artis, mood, dan hal terkait musik
        
        CONTOH INTERAKSI:
        User: "Lagi mau sarapan nih"
        Assistant: "Wah sarapan! Pasti mood kamu lagi happy ya 😊 Mau gw kasih rekomendasi lagu yang cocok buat sarapan? Biasanya lagu upbeat enak buat nemenin pagi!"
        
        User: "Siapa itu One Direction?"
        Assistant: "One Direction! Boy band legendaris dari UK yang terkenal banget tahun 2010-an. Mau gw cariin info lengkap tentang mereka?"
        
        Selalu gunakan tools yang tersedia untuk memberikan respons yang akurat dan informatif!
        """

        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=memory,
            verbose=False,
        )

        return agent

    except Exception as e:
        st.error(f"Error setting up AI agent: {str(e)}")
        return None
