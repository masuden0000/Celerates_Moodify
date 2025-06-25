from typing import Dict, List, Optional

import pandas as pd

from src.core.config import MOOD_KEYWORDS, SEARCH_AVAILABLE

# Valid moods for the system
VALID_MOODS = ["happy", "sad", "neutral"]

# =============================================================================
# CORE FUNCTIONALITY
# =============================================================================


def normalize_mood(mood: str) -> str:
    """Normalize mood string to lowercase"""
    return mood.lower().strip()


def extract_mood_from_text(text: str) -> Optional[str]:
    """Extract mood from user input"""
    text = text.lower()
    mood_scores = {}

    for mood, keywords in MOOD_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            mood_scores[mood] = score

    if mood_scores:
        return max(mood_scores.keys(), key=lambda x: mood_scores[x])
    return None


def get_song_recommendations(df: pd.DataFrame, mood: str, n: int = 5) -> List[Dict]:
    """Get song recommendations based on mood"""
    mood_norm = normalize_mood(mood) if mood else "neutral"
    if mood_norm not in VALID_MOODS:
        mood_norm = "neutral"

    # Filter songs by mood
    mood_songs = df[df["mood"] == mood_norm].copy()

    if mood_songs.empty:
        return []

    # Calculate recommendation scores
    if mood_norm == "happy":
        mood_songs["score"] = (
            mood_songs["popularity"] * 0.3
            + mood_songs["valence"] * 25
            + mood_songs["energy"] * 20
            + mood_songs["danceability"] * 15
        )
    elif mood_norm == "sad":
        mood_songs["score"] = (
            mood_songs["popularity"] * 0.4
            + (1 - mood_songs["valence"]) * 25
            + mood_songs["acousticness"] * 15
        )
    else:  # neutral
        mood_songs["score"] = (
            mood_songs["popularity"] * 0.5
            + mood_songs["danceability"] * 15
            + (1 - abs(mood_songs["valence"] - 0.5)) * 20
        )

    # Get top recommendations
    recommendations = mood_songs.nlargest(n, "score")
    return recommendations.to_dict("records")


def analyze_mood_features(df: pd.DataFrame, mood: str) -> str:
    """Analisis statistik dan contoh lagu untuk mood tertentu."""
    mood_norm = normalize_mood(mood)
    if mood_norm not in VALID_MOODS:
        extracted = extract_mood_from_text(mood)
        if extracted:
            mood_norm = extracted
        else:
            return f"Mood '{mood}' tidak dikenali."

    mood_data = df[df["mood"] == mood_norm]
    if mood_data.empty:
        return f"Tidak ada data untuk mood '{mood_norm}'"

    stats = {
        "danceability": mood_data["danceability"].mean(),
        "energy": mood_data["energy"].mean(),
        "valence": mood_data["valence"].mean(),
        "popularity": mood_data["popularity"].mean(),
        "count": len(mood_data),
    }

    sample_songs = mood_data.sample(min(3, len(mood_data)))
    output = f"\n{'='*60}\n"
    output += f"   📊 ANALISIS MUSIK UNTUK MOOD '{mood_norm.upper()}'\n"
    output += f"{'='*60}\n"

    def create_bar(value, label, emoji):
        bar_length = int(value * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        return f"{emoji} {label:<12}: [{bar}] {value:.3f}"

    output += f"\n🎵 Karakteristik Audio:\n"
    output += f"   {create_bar(stats['danceability'], 'Danceability', '💃')}\n"
    output += f"   {create_bar(stats['energy'], 'Energy', '⚡')}\n"
    output += f"   {create_bar(stats['valence'], 'Valence', '😊')}\n"
    output += f"\n📈 Statistik:\n"
    output += f"   🏆 Rata-rata Popularity: {stats['popularity']:.1f}/100\n"
    output += f"   🎼 Total Lagu: {stats['count']:,}\n"
    output += f"   📊 Persentase Dataset: {(stats['count']/len(df)*100):.1f}%\n"
    output += f"\n🎵 Contoh Lagu {mood_norm.title()}:\n"
    for i, (_, song) in enumerate(sample_songs.iterrows(), 1):
        output += f"   {i}. {song['track_name']} - {song['artist_name']}\n"
    output += f"\n{'='*60}\n"
    return output


def search_music_info(query: str) -> str:
    """Search for music information using Google search"""
    if not SEARCH_AVAILABLE:
        return "Fitur pencarian tidak tersedia. Silakan install googlesearch-python."

    try:
        import requests
        from googlesearch import search as google_search

        # Tambahkan kata kunci musik untuk hasil yang lebih relevan
        music_query = f"{query} music artist band song"

        # Get search results
        search_results = []
        for url in google_search(music_query, num_results=3, lang="id"):
            search_results.append(url)

        if not search_results:
            return (
                f"Tidak ditemukan hasil untuk '{query}'. Coba kata kunci yang berbeda."
            )

        output = f"🔍 **Hasil Pencarian untuk '{query}':**\n\n"

        for i, url in enumerate(search_results, 1):
            try:
                # Extract domain name for display
                domain = url.split("//")[1].split("/")[0] if "//" in url else url
                output += f"{i}. **{domain}**\n"
                output += f"   {url}\n\n"
            except:
                output += f"{i}. {url}\n\n"

        output += "💡 **Tips:** Klik link di atas untuk informasi lebih detail tentang musik yang kamu cari!"
        return output

    except ImportError:
        return "Modul pencarian belum terinstall. Jalankan: pip install googlesearch-python"
    except Exception as e:
        return f"Terjadi kesalahan saat mencari: {str(e)}\nCoba lagi dengan kata kunci yang berbeda."
