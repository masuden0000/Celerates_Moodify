import random
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.core.config import GENRE_EMOJIS, MOOD_EMOJIS, MOOD_KEYWORDS, SEARCH_AVAILABLE

# Valid moods for the system
VALID_MOODS = [
    "happy",
    "sad",
    "neutral",
    "energetic",
    "calm",
    "romantic",
    "melancholic",
]

# Advanced mood criteria with audio features
MOOD_CRITERIA = {
    "happy": {
        "valence": (0.5, 1.0),
        "energy": (0.4, 1.0),
        "danceability": (0.3, 1.0),
        "tempo": (80, 200),
    },
    "sad": {
        "valence": (0.0, 0.5),
        "energy": (0.0, 0.6),
        "acousticness": (0.0, 1.0),
        "tempo": (60, 120),
    },
    "energetic": {
        "energy": (0.7, 1.0),
        "danceability": (0.6, 1.0),
        "tempo": (120, 200),
        "loudness": (-10, 0),
    },
    "calm": {
        "valence": (0.3, 0.7),
        "energy": (0.0, 0.5),
        "acousticness": (0.3, 1.0),
        "tempo": (60, 100),
    },
    "romantic": {
        "valence": (0.4, 0.8),
        "energy": (0.2, 0.7),
        "acousticness": (0.2, 1.0),
        "tempo": (70, 130),
    },
    "neutral": {"valence": (0.3, 0.7), "energy": (0.3, 0.7), "tempo": (70, 140)},
}

# =============================================================================
# CORE FUNCTIONALITY
# =============================================================================


def normalize_mood(mood: str) -> str:
    """Normalize mood string to lowercase"""
    return mood.lower().strip()


def extract_mood_from_text(text: str) -> Optional[str]:
    """Extract mood from user input using advanced scoring"""
    text = text.lower()
    mood_scores = {}

    # Enhanced keyword matching with context
    context_boost = {
        "workout": "energetic",
        "gym": "energetic",
        "party": "happy",
        "galau": "sad",
        "putus": "sad",
        "sarapan": "happy",
        "makan pagi": "happy",
        "santai": "calm",
        "relax": "calm",
        "romantic": "romantic",
        "cinta": "romantic",
    }

    # Check context boost first
    for keyword, boosted_mood in context_boost.items():
        if keyword in text:
            mood_scores[boosted_mood] = mood_scores.get(boosted_mood, 0) + 3

    # Standard mood keyword matching
    for mood, keywords in MOOD_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                # Weight longer keywords more heavily
                score += len(keyword.split())
        mood_scores[mood] = mood_scores.get(mood, 0) + score

    if mood_scores:
        detected_mood = max(mood_scores.keys(), key=lambda x: mood_scores[x])
        return detected_mood if mood_scores[detected_mood] > 0 else "neutral"
    return "neutral"


def get_song_recommendations(df: pd.DataFrame, mood: str, n: int = 5) -> List[Dict]:
    """
    Advanced song recommendation system with diversified sampling
    """
    try:
        # Detect mood from text if needed
        if mood.lower() not in VALID_MOODS:
            detected_mood = extract_mood_from_text(mood)
            mood_norm = detected_mood if detected_mood else "neutral"
        else:
            mood_norm = normalize_mood(mood)

        # Apply multi-criteria filtering
        filtered_df = apply_mood_criteria(df, mood_norm)

        if filtered_df.empty:
            return []

        # Get diversified recommendations
        recommendations = get_diversified_recommendations(filtered_df, mood_norm, n)

        return recommendations.to_dict("records")

    except Exception as e:
        print(f"Error in get_song_recommendations: {str(e)}")
        return []


def apply_mood_criteria(df: pd.DataFrame, mood: str) -> pd.DataFrame:
    """
    Apply multi-criteria filtering based on audio features
    """
    criteria = MOOD_CRITERIA.get(mood, MOOD_CRITERIA["neutral"])
    filtered_df = df.copy()

    # Apply criteria for each audio feature
    for feature, (min_val, max_val) in criteria.items():
        if feature in df.columns:
            filtered_df = filtered_df[
                (filtered_df[feature] >= min_val) & (filtered_df[feature] <= max_val)
            ]

    return filtered_df


def get_diversified_recommendations(
    df: pd.DataFrame, mood: str, n_recommendations: int = 5
) -> pd.DataFrame:
    """
    Diversified sampling algorithm to avoid repetitive results
    """
    if len(df) <= n_recommendations:
        return df

    recommendations = pd.DataFrame()

    # 1. STRATIFIED SAMPLING by genre (if genre column exists)
    if "track_genre" in df.columns or "genre" in df.columns:
        genre_col = "track_genre" if "track_genre" in df.columns else "genre"
        genre_counts = df[genre_col].value_counts()
        top_genres = genre_counts.head(3).index.tolist()
        songs_per_genre = max(1, n_recommendations // len(top_genres))

        for genre in top_genres:
            genre_songs = df[df[genre_col] == genre]
            if not genre_songs.empty:
                sampled = weighted_sample(
                    genre_songs, min(songs_per_genre, len(genre_songs))
                )
                recommendations = pd.concat([recommendations, sampled])

    # 2. FILL REMAINING SLOTS with weighted random sampling
    remaining_slots = n_recommendations - len(recommendations)
    if remaining_slots > 0:
        remaining_df = (
            df[~df.index.isin(recommendations.index)]
            if not recommendations.empty
            else df
        )
        if not remaining_df.empty:
            additional = weighted_sample(
                remaining_df, min(remaining_slots, len(remaining_df))
            )
            recommendations = pd.concat([recommendations, additional])

    # 3. TEMPORAL RANDOMIZATION (use timestamp for seed)
    random.seed(int(datetime.now().timestamp()) % 1000)

    return recommendations.head(n_recommendations)


def weighted_sample(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Weighted sampling based on popularity with randomization factor
    """
    if len(df) <= n:
        return df

    # Use popularity for weighting if available
    if "popularity" in df.columns:
        # Normalize popularity to create weights
        pop_series = df["popularity"]
        max_pop = pop_series.max()

        if max_pop > 0:
            weights = pop_series / max_pop
        else:
            weights = pd.Series(np.ones(len(df)) / len(df), index=df.index)

        # Add random factor to avoid always picking the most popular
        random_factor = pd.Series(np.random.random(len(df)), index=df.index) * 0.4
        combined_weights = weights * 0.6 + random_factor * 0.4

        # Normalize weights
        combined_weights = combined_weights / combined_weights.sum()

        # Sample based on weights
        try:
            sampled_indices = np.random.choice(
                df.index, size=n, replace=False, p=combined_weights.values
            )
            return df.loc[sampled_indices]
        except:
            # Fallback to simple random sampling
            return df.sample(n=n)
    else:
        # Simple random sampling if no popularity column
        return df.sample(n=n)


def format_song_recommendations(
    recommendations: List[Dict], mood: str, original_input: str = ""
) -> str:
    """
    Format song recommendations with rich information in clean, organized format
    """
    if not recommendations:
        return f"Gak ada lagu yang cocok sama '{original_input or mood}' nih 😅\nCoba mood yang lain kayak 'happy', 'sad', atau 'energetic'!"

    mood_emoji = MOOD_EMOJIS.get(mood, "🎵")
    result = f"Nih lagu-lagu yang cocok sama mood lo {mood_emoji}:\n\n"

    for i, song in enumerate(recommendations, 1):
        # Basic song info
        track_name = song.get("track_name", song.get("name", "Unknown Song"))
        artist_name = song.get("artist_name", song.get("artists", "Unknown Artist"))
        genre = song.get("track_genre", song.get("genre", "unknown"))

        # Format main song line
        result += f"{i}. 🎵 **{track_name}** - {artist_name}\n"

        # Build info line with consistent format
        info_parts = [f"Genre: {genre}"]

        # Add tempo
        if song.get("tempo"):
            info_parts.append(f"Tempo: {song['tempo']:.0f} BPM")

        # Add popularity
        if song.get("popularity") is not None:
            info_parts.append(f"Popularity: {song['popularity']}/100")

        # Add energy with emoji
        if song.get("energy") is not None:
            energy_val = song["energy"]
            if energy_val > 0.7:
                energy_emoji = "🔥"
            elif energy_val > 0.4:
                energy_emoji = "⚡"
            else:
                energy_emoji = "🌙"
            info_parts.append(f"Energy: {energy_emoji}")

        # Join info parts with consistent separator
        result += f"   {' | '.join(info_parts)}\n\n"

    # Add contextual closing message
    closing_messages = {
        "happy": "Semoga hari lo makin cerah! ☀️",
        "sad": "Take your time, musik bisa jadi teman terbaik 🤗",
        "energetic": "Time to pump it up! 💪",
        "calm": "Perfect untuk me-time lo 🧘‍♀️",
        "romantic": "Aww, sweet banget! 💕",
        "neutral": "Enjoy the vibe! 😊",
    }

    result += closing_messages.get(mood, "Gimana, ada yang nyangkut? 😊")
    result += "\n\nMau gw cariin lagi dari vibe yang lain? Atau ada artis/genre favorit yang pengen lo denger?"

    return result


def get_enhanced_recommendations(df: pd.DataFrame, mood_input: str, n: int = 5) -> str:
    """
    Main function for getting enhanced recommendations with formatting
    """
    # Get raw recommendations
    recommendations = get_song_recommendations(df, mood_input, n)

    # Detect the mood for formatting
    detected_mood = (
        extract_mood_from_text(mood_input)
        if mood_input.lower() not in VALID_MOODS
        else mood_input.lower()
    )

    # Fallback to neutral if mood detection fails
    if detected_mood is None:
        detected_mood = "neutral"

    # Format and return results
    return format_song_recommendations(recommendations, detected_mood, mood_input)


def analyze_mood_features(df: pd.DataFrame, mood: str) -> str:
    """Analisis statistik dan contoh lagu untuk mood tertentu."""
    mood_norm = normalize_mood(mood)
    if mood_norm not in VALID_MOODS:
        extracted = extract_mood_from_text(mood)
        if extracted:
            mood_norm = extracted
        else:
            return f"Mood '{mood}' tidak dikenali."

    mood_data = (
        df[df["mood"] == mood_norm]
        if "mood" in df.columns
        else apply_mood_criteria(df, mood_norm)
    )
    if mood_data.empty:
        return f"Tidak ada data untuk mood '{mood_norm}'"

    # Calculate statistics
    stats = {}
    for feature in ["danceability", "energy", "valence", "popularity"]:
        if feature in mood_data.columns:
            stats[feature] = mood_data[feature].mean()

    stats["count"] = len(mood_data)

    sample_songs = mood_data.sample(min(3, len(mood_data)))
    output = f"\n{'='*60}\n"
    output += f"   📊 ANALISIS MUSIK UNTUK MOOD '{mood_norm.upper()}'\n"
    output += f"{'='*60}\n"

    def create_bar(value, label, emoji):
        bar_length = int(value * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        return f"{emoji} {label:<12}: [{bar}] {value:.3f}"

    output += f"\n🎵 Karakteristik Audio:\n"
    if "danceability" in stats:
        output += f"   {create_bar(stats['danceability'], 'Danceability', '💃')}\n"
    if "energy" in stats:
        output += f"   {create_bar(stats['energy'], 'Energy', '⚡')}\n"
    if "valence" in stats:
        output += f"   {create_bar(stats['valence'], 'Valence', '😊')}\n"

    output += f"\n📈 Statistik:\n"
    if "popularity" in stats:
        output += f"   🏆 Rata-rata Popularity: {stats['popularity']:.1f}/100\n"
    output += f"   🎼 Total Lagu: {stats['count']:,}\n"
    output += f"   📊 Persentase Dataset: {(stats['count']/len(df)*100):.1f}%\n"
    output += f"\n🎵 Contoh Lagu {mood_norm.title()}:\n"

    for i, (_, song) in enumerate(sample_songs.iterrows(), 1):
        track_name = song.get("track_name", song.get("name", "Unknown"))
        artist_name = song.get("artist_name", song.get("artists", "Unknown"))
        output += f"   {i}. {track_name} - {artist_name}\n"

    output += f"\n{'='*60}\n"
    return output


def search_music_info(query: str) -> str:
    """
    Advanced music information search with content extraction
    Similar to Gemini's grounding feature - searches web and provides direct answers
    """
    if not SEARCH_AVAILABLE:
        return "Fitur pencarian tidak tersedia. Silakan install googlesearch-python dan beautifulsoup4."

    try:
        import requests
        from googlesearch import search as google_search

        # Try to import BeautifulSoup for content extraction
        BeautifulSoup = None
        try:
            from bs4 import BeautifulSoup

            soup_available = True
        except ImportError:
            soup_available = False

        # Enhanced query with music-specific terms
        music_query = f"{query} music artist band song album release date"

        # Get search results
        search_results = []
        for url in google_search(music_query, num_results=5, lang="id"):
            search_results.append(url)

        if not search_results:
            return (
                f"Tidak ditemukan hasil untuk '{query}'. Coba kata kunci yang berbeda."
            )

        # Try to extract content from the first few URLs
        extracted_info = []

        for i, url in enumerate(search_results[:3]):  # Only check first 3 URLs
            try:
                # Skip certain domains that are usually not helpful
                skip_domains = [
                    "youtube.com",
                    "instagram.com",
                    "twitter.com",
                    "facebook.com",
                ]
                if any(domain in url.lower() for domain in skip_domains):
                    continue

                # Make request with proper headers
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

                response = requests.get(url, headers=headers, timeout=5)
                response.raise_for_status()

                if soup_available and BeautifulSoup:
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()

                    # Get text content
                    text = soup.get_text()

                    # Clean up text
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (
                        phrase.strip() for line in lines for phrase in line.split("  ")
                    )
                    text = " ".join(chunk for chunk in chunks if chunk)

                    # Extract relevant information (first 500 chars)
                    if len(text) > 500:
                        text = text[:500] + "..."

                    if text and len(text) > 50:  # Only include if substantial content
                        domain = (
                            url.split("//")[1].split("/")[0] if "//" in url else url
                        )
                        extracted_info.append(
                            {"domain": domain, "url": url, "content": text}
                        )

                        # If we have good content from one source, that might be enough
                        if len(extracted_info) >= 2:
                            break

            except Exception as e:
                # If individual URL fails, continue with next
                continue

        # Format response
        if extracted_info:
            output = f"🔍 **Informasi tentang '{query}':**\n\n"

            for i, info in enumerate(extracted_info, 1):
                output += f"**📄 Sumber {i}: {info['domain']}**\n"
                output += f"{info['content']}\n\n"

            output += "📚 **Sumber:**\n"
            for i, info in enumerate(extracted_info, 1):
                output += f"{i}. {info['url']}\n"

        else:
            # Fallback to link-only format if content extraction fails
            output = f"🔍 **Hasil Pencarian untuk '{query}':**\n\n"

            for i, url in enumerate(search_results[:3], 1):
                try:
                    domain = url.split("//")[1].split("/")[0] if "//" in url else url
                    output += f"{i}. **{domain}**\n"
                    output += f"   {url}\n\n"
                except:
                    output += f"{i}. {url}\n\n"

            output += "💡 **Tips:** Install beautifulsoup4 untuk mendapatkan ringkasan konten otomatis!\n"
            output += "Untuk sekarang, klik link di atas untuk informasi lebih detail."

        return output

    except ImportError:
        return "Modul pencarian belum terinstall. Jalankan: pip install googlesearch-python beautifulsoup4"
    except Exception as e:
        return f"Terjadi kesalahan saat mencari: {str(e)}\nCoba lagi dengan kata kunci yang berbeda."
