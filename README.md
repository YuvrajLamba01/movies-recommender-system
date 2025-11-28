# 🎬 CineMatch AI — Intelligent Movie Recommendation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movies-recommender-system-ggjdknuhjmqboacvkstdxo.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![API](https://img.shields.io/badge/API-TMDB-green)

**CineMatch AI** is a powerful content-based movie recommendation engine. By utilizing Natural Language Processing (NLP) and Cosine Similarity, it analyzes movie metadata (genres, keywords, cast, crew, and overview) to suggest the top 5 most relevant movies for any selection.

The application features a modern, responsive UI built with **Streamlit** and fetches real-time movie posters and ratings via the **TMDB API**.

🔗 **[Live Demo: Click Here to Try the App](https://movies-recommender-system-ggjdknuhjmqboacvkstdxo.streamlit.app/)**

---

## 🚀 Features

### 🔥 Smart ML Recommendations
* **Content-Based Filtering:** Uses a "Bag-of-Words" approach combining Overviews, Genres, Keywords, Cast, and Director.
* **Cosine Similarity:** Calculates the angle between movie vectors to find the closest matches.
* **Instant Results:** Uses a precomputed similarity matrix for sub-second responses.

### 🎥 TMDB API Integration
* Fetches high-quality **HD Posters**.
* Displays real-time **Ratings** and **Release Years**.
* Provides full movie overviews dynamically.
* *Robust error handling with retry logic for API limits.*

### 🎨 Premium Modern UI
* **Custom Styling:** Dark theme with gradient titles and card hover effects.
* **Responsive:** Fully mobile-friendly layout.
* **Smooth UX:** JavaScript integration for smooth scrolling and interactive "Show Overview" toggles.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Custom CSS & JS)
* **Language:** Python 3.x
* **Machine Learning:** Scikit-Learn (CountVectorizer, Cosine Similarity)
* **Data Processing:** Pandas, NumPy
* **API:** TMDB (The Movie Database)
* **Data Serialization:** Pickle

---

## 🧠 The Machine Learning Pipeline

The recommendation engine was built using the **TMDB 5000 Movies Dataset**. Here is the step-by-step process of how the model works:

### 1. Data Loading & Merging
We merged the `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` datasets on the `title` column to create a unified dataframe containing `movie_id`, `overview`, `genres`, `keywords`, `cast`, and `crew`.

### 2. Data Cleaning & Preprocessing
Raw data contained JSON-like strings. We converted these into usable Python lists:
* **Genres & Keywords:** Extracted names.
* **Cast:** Filtered to keep only the **top 3 actors**.
* **Crew:** Extracted only the **Director**.
* **Space Removal:** Converted "Science Fiction" → `ScienceFiction` and "Johnny Depp" → `JohnnyDepp` to create unique tokens.

### 3. Tag Creation (NLP)
We concatenated all text features into a single `tags` column:
```python
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
4. Vectorization (Bag-of-Words)
We used CountVectorizer to convert text data into numerical vectors, limiting the model to the 5000 most frequent words and removing English stop words.

Python

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
5. Similarity Calculation
We calculated the Cosine Similarity between all vectors. This resulted in a 4803 × 4803 matrix representing the distance between every movie.

Python

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
💻 How to Run Locally
Follow these steps to set up the project on your local machine.

1. Clone the Repository
Bash

git clone [https://github.com/YOUR_USERNAME/CineMatch-AI.git](https://github.com/YOUR_USERNAME/CineMatch-AI.git)
cd CineMatch-AI
2. Install Dependencies
Bash

pip install -r requirements.txt
3. Run the App
Bash

streamlit run app.py
The app will open in your browser at http://localhost:8501.

🗂️ Project Structure
Plaintext

CineMatch-AI/
│
├── app.py                # Main Streamlit application (Frontend + Backend)
├── movies.pkl            # Pickled dataframe containing movie metadata
├── similarity.pkl        # Pickled cosine similarity matrix
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
🚀 Future Enhancements
[ ] Hybrid Filtering: Combine content-based with collaborative filtering.

[ ] Search: Add functionality to search by Actor or Director.

[ ] Trailers: Embed YouTube trailers for recommendations.

[ ] Watchlist: Allow users to save movies to a list.

👨‍💻 Author
Yuvraj Lamba

Machine Learning & Frontend Developer

Passionate about AI, React, MERN Stack, and building full-stack applications.

❤️ Credits
Dataset: Kaggle TMDB 5000 Movie Dataset

API: The Movie Database (TMDB)
