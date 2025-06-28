"""
UI components - Main interface elements and data visualization
Handles charts, statistics, and interactive components
"""

from typing import Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def render_main_data_analysis(df):
    st.header("🎧 Dataset Analysis")
    
    # Enhanced metrics with colorful containers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎵 Total Songs",
            value=f"{len(df):,}",
            delta="Amazing collection!"
        )
    
    with col2:
        st.metric(
            label="🎤 Total Artists", 
            value=f"{df['artist_name'].nunique():,}",
            delta="Diverse talent!"
        )
    
    with col3:
        st.metric(
            label="🎭 Total Genres",
            value=f"{df['genre'].nunique():,}",
            delta="Musical variety!"
        )
    
    st.markdown("---")
    
    # Enhanced Mood Distribution with custom colors and animation
    st.subheader("🌈 Mood Distribution")
    mood_counts = df['mood'].value_counts()
    
    # Custom color palette for moods
    mood_colors = {
        'Happy': '#FFD700',
        'Sad': '#4169E1', 
        'Energetic': '#FF6347',
        'Calm': '#98FB98',
        'Romantic': '#FF69B4',
        'Angry': '#DC143C',
        'Melancholic': '#9370DB',
        'Upbeat': '#FFA500'
    }
    
    # Create colors list matching the mood order
    colors = [mood_colors.get(mood, '#FF6B6B') for mood in mood_counts.index]
    
    fig_mood = go.Figure(data=[go.Pie(
        labels=mood_counts.index,
        values=mood_counts.values,
        hole=.4,  # Donut chart
        marker=dict(
            colors=colors,
            line=dict(color='#FFFFFF', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, color='white', family='Arial Black'),
        hovertemplate='<b>%{label}</b><br>' +
                      'Count: %{value}<br>' +
                      'Percentage: %{percent}<br>' +
                      '<extra></extra>',
        pull=[0.1 if i == 0 else 0 for i in range(len(mood_counts))]  # Pull out the largest slice
    )])
    
    fig_mood.update_layout(
        title={
            'text': '🎭 Musical Moods Distribution',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2E4057', 'family': 'Arial Black'}
        },
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01,
            font=dict(size=12)
        ),
        annotations=[
            dict(
                text=f'Total<br><b>{len(df):,}</b><br>Songs',
                x=0.5, y=0.5,
                font_size=16,
                font_color='#2E4057',
                font_family='Arial Black',
                showarrow=False
            )
        ],
        margin=dict(t=80, b=20, l=20, r=120),
        height=500
    )
    
    st.plotly_chart(fig_mood, use_container_width=True)
    
    # Enhanced Genre Distribution with gradient colors and animation
    st.subheader("🎸 Genre Popularity")
    genre_counts = df['genre'].value_counts().nlargest(10)
    
    # Create gradient colors for bars
    colors_gradient = px.colors.sequential.Viridis_r[:len(genre_counts)]
    
    fig_genre = go.Figure(data=[
        go.Bar(
            x=genre_counts.index,
            y=genre_counts.values,
            marker=dict(
                color=colors_gradient,
                line=dict(color='rgba(255,255,255,0.8)', width=2),
                opacity=0.8
            ),
            text=genre_counts.values,
            textposition='outside',
            textfont=dict(size=12, color='#2E4057', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>' +
                          'Songs: %{y}<br>' +
                          'Percentage: %{customdata:.1f}%<br>' +
                          '<extra></extra>',
            customdata=(genre_counts.values / len(df) * 100)
        )
    ])
    
    fig_genre.update_layout(
        title={
            'text': '🎵 Top 10 Most Popular Genres',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2E4057', 'family': 'Arial Black'}
        },
        xaxis=dict(
            title=dict(
                text='Genre',
                font=dict(size=16, color='#2E4057', family='Arial Black')
            ),
            tickfont=dict(size=12, color='#2E4057'),
            tickangle=45,
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(
                text='Number of Songs',
                font=dict(size=16, color='#2E4057', family='Arial Black')
            ),
            tickfont=dict(size=12, color='#2E4057'),
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True
        ),
        plot_bgcolor='rgba(240,248,255,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(t=80, b=100, l=80, r=40),
        height=500,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    # Add animation effect
    fig_genre.update_traces(
        marker_line_width=2,
        selector=dict(type="bar")
    )
    
    st.plotly_chart(fig_genre, use_container_width=True)
    
    # Additional fun visualization: Mood vs Genre heatmap
    st.subheader("🔥 Mood-Genre Correlation Heatmap")
    
    # Create cross-tabulation
    mood_genre_crosstab = pd.crosstab(df['mood'], df['genre'])
    
    # Get top genres for better visualization
    top_genres = df['genre'].value_counts().head(8).index
    mood_genre_subset = mood_genre_crosstab[top_genres]
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=mood_genre_subset.values,
        x=mood_genre_subset.columns,
        y=mood_genre_subset.index,
        colorscale='Viridis',
        text=mood_genre_subset.values,
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white"},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b> × <b>%{x}</b><br>' +
                      'Count: %{z}<br>' +
                      '<extra></extra>'
    ))
    
    fig_heatmap.update_layout(
        title={
            'text': '🎭 Mood × Genre Combinations',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2E4057', 'family': 'Arial Black'}
        },
        xaxis=dict(
            title=dict(
                text='Genre',
                font=dict(size=16, color='#2E4057', family='Arial Black')
            ),
            tickangle=45
        ),
        yaxis=dict(
            title=dict(
                text='Mood',
                font=dict(size=16, color='#2E4057', family='Arial Black')
            )
        ),
        height=400,
        margin=dict(t=80, b=100, l=100, r=40)
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Fun stats section
    st.markdown("---")
    st.subheader("🎯 Fun Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        most_popular_mood = mood_counts.index[0]
        mood_percentage = (mood_counts.iloc[0] / len(df)) * 100
        st.info(f"🎭 **Most Popular Mood:** {most_popular_mood} ({mood_percentage:.1f}%)")
        
        most_popular_genre = genre_counts.index[0]
        genre_percentage = (genre_counts.iloc[0] / len(df)) * 100
        st.success(f"🎵 **Most Popular Genre:** {most_popular_genre} ({genre_percentage:.1f}%)")
    
    with col2:
        # Calculate some interesting stats
        unique_combinations = df.groupby(['mood', 'genre']).size().shape[0]
        st.warning(f"🎨 **Unique Mood-Genre Combinations:** {unique_combinations}")
        
        avg_songs_per_artist = len(df) / df['artist_name'].nunique()
        st.error(f"🎤 **Average Songs per Artist:** {avg_songs_per_artist:.1f}")

# MINIMALIST UI COMPONENTS

def render_statistics(df: pd.DataFrame):
    """Render minimalist app statistics"""
    analytics = st.session_state.get(
        "analytics", {"total_queries": 0, "recommendations_given": 0}
    )

    st.markdown(
        f"""
    <div class="stats-container">
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-value">{len(df):,}</span>
                <div class="stat-label">Songs</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{df['artist_name'].nunique():,}</span>
                <div class="stat-label">Artists</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{df['genre'].nunique():,}</span>
                <div class="stat-label">Genres</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{analytics['total_queries']:,}</span>
                <div class="stat-label">Queries</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
