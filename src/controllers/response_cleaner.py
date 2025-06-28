"""
Response cleaner - Text processing and cleaning utilities
Handles AI response formatting and cleanup
"""

import re

def clean_agent_response(response: str) -> str:
    """
    Membersihkan response dari semua debugging output dengan intelligent handling
    """
    # Check if this is a lyrics search confirmation response
    if is_lyrics_confirmation_response(response):
        # For lyrics search, only extract the Final Answer and convert thought to friendly response
        return extract_and_convert_lyrics_response(response)

    # Hapus semua pattern debugging LangChain
    patterns_to_remove = [
        r"Thought:.*?(?=\n|$)",
        r"Do I need to use a tool\?.*?(?=\n|$)",
        r"Action:.*?(?=\n|$)",
        r"Action Input:.*?(?=\n|$)",
        r"Observation:.*?(?=\n|$)",
        r"Final Answer:\s*",  # Remove "Final Answer:" label but keep content
        r"I need to.*?(?=\n|$)",
        r"Let me.*?(?=\n|$)",
        r"I should.*?(?=\n|$)",
        r"\*\*Koreksi:\*\*[^\n]*→[^\n]*(?=\n|$)",  # Remove correction lines
    ]

    cleaned = response

    # Remove all debugging patterns
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)

    # Clean up whitespace
    cleaned = re.sub(r"\n\s*\n\s*\n", "\n\n", cleaned)  # Max 2 newlines
    cleaned = re.sub(r"^\s+|\s+$", "", cleaned)  # Trim start/end

    # Jika response masih kosong atau hanya debugging, return fallback
    if not cleaned or len(cleaned.strip()) < 10:
        return "Maaf, ada masalah dengan response. Coba input lagi ya! 😅"

    return cleaned

def is_lyrics_confirmation_response(response: str) -> bool:
    """Check if this is a lyrics search response that should be shown to user"""
    lyrics_indicators = [
        "🎵 **Pencarian Lirik:**",
        "**Judul:**",
        "**Artis:**",
        "**Lirik:**",
        "**Koreksi:**",
        "Pencarian Lirik:",
        "lirik lagu",
        "lyrics",
        # Remove old confirmation patterns to avoid blocking direct lyrics
        # "Apakah yang kamu maksudkan adalah",
        # "Apakah yang kamu maksud adalah",
        # "sepertinya ada typo",
        # "Ketik 'ya' untuk konfirmasi",
        # "konfirmasi pencarian",
    ]

    return any(indicator in response for indicator in lyrics_indicators)

def extract_and_convert_lyrics_response(response: str) -> str:
    """
    Extract lyrics response and ensure it's displayed directly to user
    """
    # Extract the Final Answer first
    final_answer_match = re.search(
        r"Final Answer:\s*(.*)", response, re.DOTALL | re.IGNORECASE
    )

    if final_answer_match:
        final_answer = final_answer_match.group(1).strip()

        # If Final Answer contains lyrics content, return it directly
        if is_lyrics_confirmation_response(final_answer):
            return final_answer  # Return lyrics directly without conversion

        return final_answer

    # If no Final Answer, check if raw response contains lyrics
    if is_lyrics_confirmation_response(response):
        return response  # Return lyrics directly

    return clean_agent_response(response)

def make_lyrics_confirmation_friendly(text: str) -> str:
    """Convert formal confirmation to friendly AI response"""
    # Extract the corrected song name
    song_match = re.search(r"\*\*(.*?)\*\*", text)

    if song_match:
        corrected_song = song_match.group(1)

        friendly_response = f"Eh, kayaknya ada typo dikit nih di nama lagunya 😅 Lo maksudnya **'{corrected_song}'** kah? "
        friendly_response += "Kalau iya, ketik 'ya' aja buat gw cariin liriknya. "
        friendly_response += (
            "Kalau bukan, coba ketik ulang ya dengan ejaan yang lebih jelas! 🎵"
        )

        return friendly_response

    # Fallback: just clean the original text
    return re.sub(
        r"Thought:.*?(?=\n|$)", "", text, flags=re.IGNORECASE | re.MULTILINE
    ).strip()

def extract_final_answer(response: str) -> str:
    """
    Extract only the final answer part from agent response with intelligent handling
    """
    # Special handling for lyrics search responses
    if is_lyrics_confirmation_response(response):
        return extract_and_convert_lyrics_response(response)

    # Cari pattern "Final Answer:" dan ambil setelahnya
    final_answer_match = re.search(
        r"Final Answer:\s*(.*)", response, re.DOTALL | re.IGNORECASE
    )

    if final_answer_match:
        final_answer = final_answer_match.group(1).strip()

        # For lyrics responses, check if it's already clean format from Gemini
        if "🎵 **Pencarian Lirik:**" in final_answer:
            # Extract just the Gemini result, not agent's override
            gemini_match = re.search(
                r"🎵 \*\*Pencarian Lirik:\*\*.*?(?=🎵|\Z)", final_answer, re.DOTALL
            )
            if gemini_match:
                return gemini_match.group(0).strip()

        return final_answer

    # Jika tidak ada Final Answer, clean response biasa
    return clean_agent_response(response)
