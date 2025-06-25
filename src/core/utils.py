from datetime import datetime

import pandas as pd
import streamlit as st

from src.core.music_analyzer import (
    analyze_mood_features,
    extract_mood_from_text,
    get_song_recommendations,
    search_music_info,
)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def get_ai_response(agent, user_input: str, df: pd.DataFrame) -> tuple:
    """Get response from AI agent or fallback to basic responses"""

    # Update analytics
    if "analytics" not in st.session_state:
        st.session_state.analytics = {"total_queries": 0, "recommendations_given": 0}

    st.session_state.analytics["total_queries"] += 1

    if agent:
        try:
            response = agent.invoke({"input": user_input})
            ai_response = response.get("output", "Sorry, I encountered an error.")

            # Check if response contains analysis output that should be displayed as-is
            if (
                "ANALYSIS_OUTPUT_START" in ai_response
                and "ANALYSIS_OUTPUT_END" in ai_response
            ):
                # Extract the analysis content between the tags
                start_tag = "ANALYSIS_OUTPUT_START\n"
                end_tag = "\nANALYSIS_OUTPUT_END"
                start_idx = ai_response.find(start_tag)
                end_idx = ai_response.find(end_tag)

                if start_idx != -1 and end_idx != -1:
                    # Get the pure analysis output
                    analysis_content = ai_response[start_idx + len(start_tag) : end_idx]
                    return analysis_content, []

            # Check if recommendations should be shown
            detected_mood = extract_mood_from_text(user_input)
            recommendations = []
            if detected_mood and any(
                word in user_input.lower()
                for word in ["recommend", "song", "music", detected_mood]
            ):
                recommendations = get_song_recommendations(df, detected_mood, 3)
                st.session_state.analytics["recommendations_given"] += len(
                    recommendations
                )

            return ai_response, recommendations

        except Exception as e:
            st.error(f"AI Agent error: {str(e)}")
            return get_basic_response(user_input, df)
    else:
        return get_basic_response(user_input, df)


def get_basic_response(user_input: str, df: pd.DataFrame) -> tuple:
    """Get basic response without AI agent dengan bahasa Indonesia"""
    user_input_lower = user_input.lower()

    # Cek jika pertanyaan di luar konteks musik
    non_music_keywords = [
        "cuaca",
        "weather",
        "politik",
        "politik",
        "olahraga",
        "sport",
        "berita",
        "news",
        "makanan",
        "food",
        "film",
        "movie",
        "game",
        "coding",
        "programming",
        "matematika",
        "math",
    ]

    if any(keyword in user_input_lower for keyword in non_music_keywords):
        return (
            "Sorry bro, gw agent khusus musik nih! 🎵 Tanya aja yang berhubungan sama lagu, artis, atau mood musik ya!",
            [],
        )

    # Detect mood
    detected_mood = extract_mood_from_text(user_input)

    if detected_mood:
        mood_responses = {
            "happy": "Wah mood kamu lagi happy nih! 😊 Nih gw kasih lagu-lagu upbeat yang cocok buat kamu!",
            "sad": "Hmm sepertinya lagi sedih ya? 😢 Gw punya lagu-lagu yang mungkin bisa nemenin perasaan kamu.",
            "neutral": "Mood kamu lagi santai ya! 😌 Perfect nih buat lagu-lagu chill yang enak didengar.",
        }

        response = mood_responses.get(
            detected_mood,
            f"Oke, gw cariin lagu-lagu yang cocok buat mood '{detected_mood}' kamu ya! 🎵",
        )
        recommendations = get_song_recommendations(df, detected_mood, 5)
        st.session_state.analytics["recommendations_given"] += len(recommendations)

        return response, recommendations

    # Pattern matching untuk query lainnya
    if any(word in user_input_lower for word in ["hello", "hi", "hey", "halo", "hai"]):
        return (
            "Halo! 👋 Gw Moodify, AI assistant musik kamu! Cerita dong mood kamu gimana hari ini? Atau mau tanya tentang musik apa? 🎵",
            [],
        )

    if any(
        word in user_input_lower
        for word in ["analyze", "analysis", "analisis", "features", "fitur"]
    ):
        mood = extract_mood_from_text(user_input) or "happy"
        analysis = analyze_mood_features(df, mood)
        return analysis, []

    if any(
        word in user_input_lower for word in ["search", "find", "cari", "info", "siapa"]
    ):
        # Ekstrak query untuk pencarian
        search_query = (
            user_input.replace("cari", "")
            .replace("siapa", "")
            .replace("info", "")
            .strip()
        )
        if search_query:
            search_result = search_music_info(search_query)
            return search_result, []
        else:
            return (
                "Mau cari info tentang apa? Kasih tau gw nama artis, band, atau lagu yang mau kamu tau! 🔍",
                [],
            )

    # Jika input mengandung kata rekomendasi atau request lagu
    if any(
        word in user_input_lower
        for word in ["rekomendasi", "recommend", "lagu", "musik", "song", "music"]
    ):
        # Coba deteksi mood dari konteks
        detected_mood = extract_mood_from_text(user_input) or "happy"
        recommendations = get_song_recommendations(df, detected_mood, 5)
        st.session_state.analytics["recommendations_given"] += len(recommendations)
        return (
            f"Nih gw kasih rekomendasi lagu yang cocok buat kamu! 🎵",
            recommendations,
        )

    return (
        "Hmm, gw kurang ngerti nih 🤔 Tapi tenang aja! Cerita dong mood kamu gimana, atau mau tanya tentang musik apa? Gw bisa kasih rekomendasi lagu, analisis musik, atau cari info tentang artis favorit kamu! 🎵",
        [],
    )


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "bot",
                "content": "Halo! 👋 Gw Moodify, AI assistant musik kamu! Gimana mood kamu hari ini? Atau ada yang mau ditanyain tentang musik? 🎵",
                "timestamp": datetime.now(),
            }
        ]

    if "df" not in st.session_state:
        st.session_state.df = None

    if "agent" not in st.session_state:
        st.session_state.agent = None

    if "analytics" not in st.session_state:
        st.session_state.analytics = {"total_queries": 0, "recommendations_given": 0}


def process_user_input(user_input: str, agent, df: pd.DataFrame):
    """Process user input and update chat"""

    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "timestamp": datetime.now()}
    )

    # Get AI response
    with st.spinner("Sedang mikir..."):
        response, recommendations = get_ai_response(agent, user_input, df)

    # Add bot response
    bot_message = {"role": "bot", "content": response, "timestamp": datetime.now()}

    if recommendations:
        bot_message["recommendations"] = recommendations

    st.session_state.messages.append(bot_message)

    # Rerun to show new messages
    st.rerun()
