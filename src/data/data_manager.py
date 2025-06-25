import numpy as np
import pandas as pd
import streamlit as st

# =============================================================================
# DATA MANAGEMENT
# =============================================================================


@st.cache_data
def load_music_data():
    """Load or generate music dataset"""
    try:
        df = pd.read_csv("spotify_data.csv")
        st.success("✅ Loaded music data from CSV")
    except FileNotFoundError:
        st.info("📊 Creating sample music dataset...")
        df = create_sample_data()

    return process_music_data(df)


def create_sample_data():
    """Create sample music dataset"""
    np.random.seed(42)

    artists = [
        "Taylor Swift",
        "Drake",
        "Billie Eilish",
        "The Weeknd",
        "Ariana Grande",
        "Post Malone",
        "Dua Lipa",
        "Ed Sheeran",
        "Harry Styles",
        "BTS",
    ]

    genres = ["Pop", "Hip-Hop", "R&B", "Rock", "Electronic", "Indie", "K-Pop"]
    n_songs = 300

    df = pd.DataFrame(
        {
            "track_name": [f"Song {i}" for i in range(1, n_songs + 1)],
            "artist_name": np.random.choice(artists, n_songs),
            "genre": np.random.choice(genres, n_songs),
            "valence": np.random.beta(2, 2, n_songs),
            "energy": np.random.beta(2, 2, n_songs),
            "danceability": np.random.beta(2, 2, n_songs),
            "acousticness": np.random.beta(1.5, 3, n_songs),
            "tempo": np.random.normal(120, 30, n_songs).clip(60, 200),
            "popularity": np.random.gamma(2, 20, n_songs).clip(0, 100).astype(int),
            "release_year": np.random.randint(2000, 2024, n_songs),
            "duration_ms": np.random.normal(210000, 60000, n_songs)
            .clip(30000, 600000)
            .astype(int),
        }
    )

    return df


def process_music_data(df):
    """Process and enhance music data"""

    # Add mood classification
    def classify_mood(row):
        if row["valence"] >= 0.6 and row["energy"] >= 0.6:
            return "happy"
        elif row["valence"] <= 0.4 or row["energy"] <= 0.3:
            return "sad"
        else:
            return "neutral"

    df["mood"] = df.apply(classify_mood, axis=1)
    df["duration_min"] = (df["duration_ms"] / 1000 / 60).round(2)

    return df
