"""
Controller utilities - Session management and user input processing
Handles core application logic and workflow coordination
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from src.models.music_analyzer import (
    analyze_mood_features,
    extract_mood_from_text,
    get_song_recommendations,
    search_music_info,
)

# UTILITY FUNCTIONS


def get_ai_response(agent, user_input: str, df: pd.DataFrame) -> tuple:
    """Get response from AI agent or fallback to basic responses"""

    # Check for lyrics confirmation context first
    lyrics_confirmation_response = handle_lyrics_confirmation_context(user_input)
    if lyrics_confirmation_response:
        return lyrics_confirmation_response, []  # Update analytics
    if "analytics" not in st.session_state:
        st.session_state.analytics = {"total_queries": 0, "recommendations_given": 0}

    st.session_state.analytics["total_queries"] += 1

    if agent:
        try:
            response = agent.invoke({"input": user_input})
            ai_response = response.get(
                "output", "Sorry, I encountered an error."
            )  # Clean response dari debugging output dengan intelligent handling
            from src.controllers.response_cleaner import (
                clean_agent_response,
                extract_final_answer,
                is_lyrics_confirmation_response,
            )

            cleaned_response = extract_final_answer(ai_response)

            # Special handling untuk lyrics search - langsung return tanpa cleaning tambahan
            if is_lyrics_confirmation_response(
                cleaned_response
            ) or is_lyrics_confirmation_response(ai_response):
                # Return langsung untuk lyrics responses
                return (
                    cleaned_response
                    if is_lyrics_confirmation_response(cleaned_response)
                    else ai_response
                ), []

            # Jika masih ada debugging info yang bukan lyrics confirmation, paksa clean
            if any(
                debug_word in cleaned_response.lower()
                for debug_word in ["thought:", "action:", "do i need"]
            ):
                cleaned_response = clean_agent_response(cleaned_response)

            # Check if response contains analysis output that should be displayed as-is
            if (
                "ANALYSIS_OUTPUT_START" in cleaned_response
                and "ANALYSIS_OUTPUT_END" in cleaned_response
            ):
                # Extract the analysis content between the tags
                start_tag = "ANALYSIS_OUTPUT_START\n"
                end_tag = "\nANALYSIS_OUTPUT_END"
                start_idx = cleaned_response.find(start_tag)
                end_idx = cleaned_response.find(end_tag)

                if start_idx != -1 and end_idx != -1:
                    # Get the pure analysis output
                    analysis_content = cleaned_response[
                        start_idx + len(start_tag) : end_idx
                    ]
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

            return cleaned_response, recommendations

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

    # Sync with current chat session after messages are added
    from src.views.sidebar import sync_current_chat

    sync_current_chat()

    # Rerun to show new messages
    st.rerun()


# LYRICS SEARCH CONTEXT MANAGEMENT


def handle_lyrics_confirmation_context(user_input: str) -> str:
    """
    Handle lyrics search confirmation context

    Args:
        user_input: User input that might be a confirmation

    Returns:
        Response or empty string if not a confirmation
    """
    # Check if we're in lyrics confirmation context
    if "lyrics_confirmation_query" not in st.session_state:
        return ""

    # Check if user is confirming
    confirmation_words = ["ya", "iya", "yes", "benar", "betul", "ok", "oke", "confirm"]
    denial_words = ["tidak", "no", "bukan", "gak", "enggak", "salah"]

    user_lower = user_input.lower().strip()

    if any(word in user_lower for word in confirmation_words):
        # User confirmed, search with corrected query
        query = st.session_state.lyrics_confirmation_query
        del (
            st.session_state.lyrics_confirmation_query
        )  # Clear confirmation context        # Import lyrics service from the new MVC structure
        from src.services.lyrics_service import search_lyrics_with_gemini

        # Force search without asking for confirmation again
        st.session_state.lyrics_skip_confirmation = True
        result = search_lyrics_with_gemini(query)
        if "lyrics_skip_confirmation" in st.session_state:
            del st.session_state.lyrics_skip_confirmation

        return result

    elif any(word in user_lower for word in denial_words):
        # User denied, clear context
        del st.session_state.lyrics_confirmation_query
        return "👍 No problem! Coba ketik query pencarian lirik yang baru ya. Format: 'lirik [judul lagu] - [nama artis]'"

    return ""


def is_lyrics_query(query: str) -> bool:
    """Check if query is asking for lyrics"""
    lyrics_keywords = [
        "lirik",
        "lyrics",
        "chord",
        "kord",
        "kata-kata",
        "syair",
        "teks lagu",
        "kata lagu",
        "lirik lagu",
    ]

    return any(keyword in query.lower() for keyword in lyrics_keywords)
