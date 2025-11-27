import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import streamlit.components.v1 as components  # Required for JavaScript injection

# ------------------ CONFIGURATION & STYLING ------------------
st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a "Perfect" UI
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }

    /* Hide Streamlit Header/Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Typography */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        padding-bottom: 20px;
        background: -webkit-linear-gradient(45deg, #ff4b4b, #ff9068);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h3 {
        color: #e0e0e0;
        font-weight: 300;
    }

    /* Custom Card Style for Movies */
    .movie-card {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 0px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        overflow: hidden;
        margin-bottom: 15px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.5);
    }

    .movie-info {
        padding: 15px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .movie-title {
        color: #fff;
        font-weight: bold;
        font-size: 1.05rem;
        margin-bottom: 5px;
        line-height: 1.4;
    }

    .match-score {
        background-color: #4CAF50;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
        align-self: flex-start;
    }

    .movie-meta {
        color: #9ca3af;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #374151;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff9068 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        font-weight: bold;
        border-radius: 30px;
        cursor: pointer;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
        color: white;
    }

    /* Overview Container Styling */
    .overview-container {
        background-color: #1f2937;
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        border-left: 5px solid #ff4b4b;
        animation: fadeIn 0.5s;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

</style>
""", unsafe_allow_html=True)

# ------------------ TMDB API SETUP ------------------
TMDB_API_KEY = "0008464023f584902a7de27b9f6787e5"
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie/{}"
IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"
FALLBACK_POSTER = "https://via.placeholder.com/500x750?text=No+Image"

retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)


# ------------------ FUNCTIONS ------------------

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id: int):
    """
    Fetches comprehensive details: Poster, Overview, Rating, Date.
    """
    url = TMDB_MOVIE_URL.format(movie_id)
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}

    try:
        resp = session.get(url, params=params, timeout=3)
        resp.raise_for_status()
        data = resp.json()

        poster_path = data.get("poster_path")
        poster_url = IMG_BASE_URL + poster_path if poster_path else FALLBACK_POSTER

        return {
            "poster": poster_url,
            "overview": data.get("overview", "No overview available."),
            "rating": round(data.get("vote_average", 0), 1),
            "date": data.get("release_date", "Unknown")[:4]  # Just the year
        }

    except Exception:
        return {
            "poster": FALLBACK_POSTER,
            "overview": "Details unavailable.",
            "rating": "N/A",
            "date": "N/A"
        }


def get_recommendations(movie_title, movies_df, similarity_matrix):
    """
    Returns list of dicts with title, id, and match score.
    """
    try:
        movie_index = movies_df[movies_df['title'] == movie_title].index[0]
        distances = similarity_matrix[movie_index]

        # Sort by similarity (highest first), skip the first one (itself)
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommendations = []
        for idx, score in movies_list:
            row = movies_df.iloc[idx]
            recommendations.append({
                "title": row.title,
                "id": int(row.movie_id),
                "match_score": int(score * 100)  # Convert 0.85 -> 85%
            })
        return recommendations
    except IndexError:
        return []


# ------------------ DATA LOADING (WITH FALLBACK) ------------------

@st.cache_resource
def load_data():
    """
    Loads pickles. If missing, creates dummy data so the UI still works for demo.
    """
    try:
        movies_dict = pickle.load(open("movies.pkl", "rb"))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open("similarity.pkl", "rb"))
        return movies, similarity
    except FileNotFoundError:
        st.warning("⚠️ 'movies.pkl' or 'similarity.pkl' not found. Using Mock Data for UI demonstration.")
        # Create Mock Data
        mock_movies = pd.DataFrame({
            'title': ['Avatar', 'Titanic', 'The Avengers', 'Inception', 'Interstellar', 'The Dark Knight'],
            'movie_id': [19995, 597, 24428, 27205, 157336, 155]
        })
        # Mock Similarity Matrix (6x6)
        import numpy as np
        mock_sim = np.random.rand(6, 6)
        np.fill_diagonal(mock_sim, 1.0)
        return mock_movies, mock_sim


movies, similarity = load_data()
movie_titles = movies['title'].values

# ------------------ MAIN UI LAYOUT ------------------

# 1. Hero Section
st.markdown("<h1>🎬 CineMatch AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; margin-bottom: 40px;'>Discover your next favorite film using Content-Based Filtering</h3>",
    unsafe_allow_html=True)

# 2. Search Area (Centered)
col_spacer_l, col_input, col_spacer_r = st.columns([1, 2, 1])
with col_input:
    selected_movie_name = st.selectbox(
        "Type or select a movie you like:",
        movie_titles,
        index=0,
        help="Start typing to search your movie database"
    )

    st.write("")  # Spacer
    if st.button("🚀 Find Recommendations"):
        with st.spinner('Analyzing patterns and fetching metadata...'):
            recommendations = get_recommendations(selected_movie_name, movies, similarity)

            # Fetch details for all recommendations
            results_data = []
            for rec in recommendations:
                details = fetch_movie_details(rec['id'])
                rec.update(details)
                results_data.append(rec)

            # Save to session state so data persists when we click overview buttons
            st.session_state['results_data'] = results_data
            # Clear previous overview selection
            if 'selected_overview' in st.session_state:
                del st.session_state['selected_overview']

            # --- NEW: Flag to trigger scroll ---
            st.session_state['scroll_to_results'] = True

if 'results_data' in st.session_state:

    # --- NEW: Scroll Target Anchor ---
    st.markdown('<div id="results-target"></div>', unsafe_allow_html=True)

    st.markdown("### Top Picks for You")
    results_data = st.session_state['results_data']

    # 3. Results Display (Responsive Cards)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        if idx < len(results_data):
            movie = results_data[idx]
            with col:
                # Rendering an HTML card inside the column
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{movie['poster']}" style="width:100%; height:300px; object-fit: cover; border-radius: 12px 12px 0 0;">
                    <div class="movie-info">
                        <div class="match-score">{movie['match_score']}% Match</div>
                        <div class="movie-title" title="{movie['title']}">{movie['title']}</div>
                        <div class="movie-meta">
                            <span>📅 {movie['date']}</span>
                            <span>⭐ {movie['rating']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # REPLACED st.expander WITH BUTTON
                if st.button("Show Overview", key=f"btn_{idx}", use_container_width=True):
                    st.session_state['selected_overview'] = movie

    # --- NEW: JS Scroll Logic for Results ---
    if st.session_state.get('scroll_to_results', False):
        components.html(
            """
            <script>
                setTimeout(function() {
                    const element = window.parent.document.getElementById('results-target');
                    if (element) {
                        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 100);
            </script>
            """,
            height=0,
            width=0
        )
        # Reset the flag so it doesn't scroll again on subsequent clicks
        st.session_state['scroll_to_results'] = False

    # 4. Wide Overview Section (Displayed BELOW the columns)
    if 'selected_overview' in st.session_state:
        sel_movie = st.session_state['selected_overview']
        st.markdown("---")

        # --- SCROLL TARGET ID ---
        st.markdown('<div id="overview-scroll-target"></div>', unsafe_allow_html=True)

        st.subheader(f"📖 Overview: {sel_movie['title']}")

        # Display the wide text container
        st.markdown(f"""
        <div class="overview-container">
            <p style="color: #e0e0e0; font-size: 1.1rem; line-height: 1.6;">
                {sel_movie['overview']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- JS SCROLL LOGIC ---
        # We use window.parent.document to access the main DOM from the component iframe
        components.html(
            """
            <script>
                // Add a small delay to ensure element is rendered
                setTimeout(function() {
                    const element = window.parent.document.getElementById('overview-scroll-target');
                    if (element) {
                        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 100);
            </script>
            """,
            height=0,
            width=0
        )

        # Button to close the overview
        if st.button("Close Overview"):
            del st.session_state['selected_overview']
            st.rerun()

# 4. Footer info
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>Powered by TMDB API & Streamlit | ML Content-Based Filtering System</small>
</div>
""", unsafe_allow_html=True)