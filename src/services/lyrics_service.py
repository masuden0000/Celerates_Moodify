"""
Lyrics service - Song lyrics search and processing
Handles lyrics retrieval with AI-powered typo correction
"""

import re
from typing import Dict, Optional, Tuple
from urllib.parse import quote_plus

import requests
import streamlit as st

# GEMINI-POWERED LYRICS SEARCH

class GeminiLyricsSearcher:
    """Enhanced lyrics searcher using Gemini AI for typo correction and web search"""

    def __init__(self):
        self.gemini_api_key = self._get_gemini_api_key()

    def _get_gemini_api_key(self) -> Optional[str]:
        """Get Gemini API key from secrets or environment"""
        try:
            # Try new naming convention first
            gemini_key = st.secrets.get("GEMINI_API_KEY")
            if gemini_key:
                return gemini_key

            # Fallback to old naming for backward compatibility
            api_key = st.secrets.get("api_key")
            if api_key:
                return api_key

            return None
        except:
            import os

            # Try environment variables
            return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    def _correct_and_search_with_gemini(self, query: str) -> Tuple[str, str]:
        """Use Gemini to correct typos and search for lyrics directly"""
        try:
            try:
                import google.generativeai as genai  # type: ignore
            except ImportError:
                return (
                    query,
                    "❌ Google Generative AI library tidak tersedia. Install dengan: pip install google-generativeai",
                )

            if not self.gemini_api_key:
                return (
                    query,
                    "❌ Gemini API key tidak tersedia. Silakan set GEMINI_API_KEY di .streamlit/secrets.toml",
                )

            # Configure Gemini
            genai.configure(api_key=self.gemini_api_key)  # type: ignore
            model = genai.GenerativeModel("gemini-2.0-flash")  # type: ignore

            # Enhanced prompt for typo correction and lyrics search
            correction_prompt = f"""
            Tugas: Cari lirik lagu berdasarkan query pencarian. Koreksi typo HANYA jika benar-benar diperlukan.
            
            Query: "{query}"
            
            Instruksi:
            1. Identifikasi judul lagu dan artis dari query
            2. Koreksi typo HANYA jika ada kesalahan ejaan yang jelas dan signifikan
            3. Berikan informasi lagu dan seluruh lirik (lengkap)
            
            Format output:
            🎵 **Pencarian Lirik:**
            
            **Judul:** [Judul lagu yang benar]
            **Artis:** [Nama artis]
            
            **Informasi Lirik:**
            [Berikan informasi tentang lagu dan beberapa kata kunci dari lirik, BUKAN lirik lengkap]
            
            **Link Pencarian:**
            - Google: https://www.google.com/search?q=[judul] [artis] lyrics
            - Genius: https://genius.com/search?q=[judul] [artis]
            
            PENTING: 
            - HANYA tampilkan koreksi jika ada typo yang signifikan (misal: "photograf" → "photograph")
            - JANGAN tampilkan koreksi untuk hal kecil atau ejaan yang sudah benar
            - Berikan informasi lagu dan petunjuk pencarian, bukan lirik lengkap
            - Format yang bersih tanpa debugging info
            """

            response = model.generate_content(correction_prompt)

            if response and response.text:
                return query, response.text.strip()
            else:
                return query, "❌ Tidak dapat mengakses Gemini untuk pencarian lirik"

        except ImportError:
            return (
                query,
                "❌ Google Generative AI library tidak tersedia. Install dengan: pip install google-generativeai",
            )
        except Exception as e:
            return query, f"❌ Error Gemini API: {str(e)}"

    def _fallback_web_search_simulation(self, query: str) -> str:
        """Fallback web search simulation if Gemini fails"""
        try:
            # Clean query for web search
            clean_query = re.sub(
                r"\b(lirik|lyrics|chord|kord)\b", "", query, flags=re.IGNORECASE
            ).strip()
            search_query = f"{clean_query} lyrics"

            response = f"""
🎵 **Pencarian Lirik:**

**Informasi:** Pencarian melalui web search

**Link Pencarian:**
- Google: https://www.google.com/search?q={quote_plus(search_query)}
- Genius: https://genius.com/search?q={quote_plus(clean_query)}
- AZLyrics: https://search.azlyrics.com/search.php?q={quote_plus(clean_query)}

� **Tips Pencarian:**
- Gunakan format: "judul lagu artis lyrics"
- Pastikan ejaan nama artis dan judul lagu benar
- Coba variasi nama lagu jika tidak ditemukan
            """

            return response

        except Exception as e:
            return f"❌ Error dalam fallback search: {str(e)}"

# MAIN SEARCH FUNCTION

def search_lyrics_with_gemini(query: str) -> str:
    """
    Main function for lyrics search using Gemini AI

    Args:
        query: Song search query (e.g., "shape of you ed sheeran", "right no one direction")

    Returns:
        Formatted lyrics result with typo correction
    """
    searcher = GeminiLyricsSearcher()

    # Extract song info from lyrics query
    song_query = extract_song_from_query(query)

    # Use Gemini for correction and search
    corrected_query, gemini_result = searcher._correct_and_search_with_gemini(
        song_query
    )

    # Check if Gemini provided lyrics
    if gemini_result and not gemini_result.startswith("❌"):
        return gemini_result
    else:
        # Fallback to web search simulation
        fallback_result = searcher._fallback_web_search_simulation(song_query)
        return f"{gemini_result}\n\n---\n\n{fallback_result}"

def extract_song_from_query(query: str) -> str:
    """Extract song information from lyrics query"""
    # Remove lyrics-related words
    cleaned = re.sub(
        r"\b(lirik|lyrics|chord|kord|kata-kata|syair|teks|kata|lagu)\b",
        "",
        query,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned if cleaned else query

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
