🎬 CineMatch AI — Movie Recommendation System
🚀 Streamlit App • Machine Learning • TMDB API 

CineMatch AI is an intelligent movie recommendation system that helps users discover similar movies using content-based filtering, NLP, and cosine similarity.
The app features a modern Streamlit UI, real-time TMDB API posters & data, and a fast, precomputed ML model.

🔗 Live App: https://movies-recommender-system-ggjdknuhjmqboacvkstdxo.streamlit.app/

📦 Tech Stack: Python, Streamlit, Scikit-Learn, Pandas, TMDB API
🧠 Model: NLP → Bag-of-Words (5000 tokens) → Cosine Similarity



⭐ Features
🔥 Smart ML Recommendations

Top 5 similar movies using cosine similarity

Precomputed similarity matrix for instant results

Content-based filtering (overview + genres + keywords + cast + director)

🎥 TMDB API Integration

HD posters

Ratings

Release year

Full movie overview

🎨 Premium Modern UI

Custom CSS styling (cards, shadows, animations)

Responsive design (mobile-friendly)

Smooth scroll using JavaScript

Gradient titles

Interactive “Show Overview” cards

⚡ Fast & Lightweight

Uses .pkl files for ultra-fast loading

Optimized queries

Robust fallback when TMDB fails

🧠 Machine Learning Pipeline

Your ML model was built entirely from the TMDB 5000 Movies Dataset.

1️⃣ Load and Merge Data

Datasets used:

tmdb_5000_movies.csv

tmdb_5000_credits.csv

Merged on title:

movies = movies.merge(credits, on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

2️⃣ Clean JSON-like Columns → Python Lists

Using ast.literal_eval:

Genres & Keywords
def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

Cast — keep top 3 actors
movies['cast'] = movies['cast'].apply(lambda x: x[:3])

Crew — extract only Director(s)
def fetch_director(text):
    return [i['name'] for i in ast.literal_eval(text) if i['job']=='Director']

3️⃣ Remove Spaces in Names
def collapse(L):
    return [i.replace(" ","") for i in L]


Examples:

"Science Fiction" → ScienceFiction

"Johnny Depp" → JohnnyDepp

4️⃣ NLP Tag Creation

Overview → tokenized
Genres → cleaned
Keywords → keywords
Cast → top actors
Crew → director(s)

Combine everything:

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new['tags'] = new['tags'].apply(lambda x: " ".join(x))


Each movie now has a rich text representation.

5️⃣ Vectorization (Bag-of-Words)
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()

6️⃣ Cosine Similarity Matrix
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)


Creates a 4803 × 4803 matrix of similarity scores.

7️⃣ Recommend Function
def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True,
                       key=lambda x: x[1])[1:6]
    return distances


Returns top 5 most similar movies.

8️⃣ Save Final Model for Deployment
pickle.dump(new, open('movies.pkl','wb'))
pickle.dump(similarity, open('similarity.pkl','wb'))


The Streamlit app loads these instantly.

🎨 Streamlit Application

Your app.py includes:

✔ Custom CSS

Card hover effects

Dark theme

Gradient headings

Match score highlights

Overview container styling

Responsive layout

✔ JavaScript for Smooth Scroll

components.html() used to scroll to:

Results section

Overview section

✔ API Retry Logic

Handles TMDB rate-limit & retries:

retry_strategy = Retry(total=3, backoff_factor=0.5)

🗂 Project Structure
CineMatch-AI/
│
├── app.py               # Streamlit Frontend + Backend
├── movies.pkl           # Preprocessed movie metadata
├── similarity.pkl       # Cosine similarity matrix
├── requirements.txt     # Clean deployment dependencies
└── README.md            # Documentation

💻 Run Locally
git clone https://github.com/<your-username>/CineMatch-AI.git
cd CineMatch-AI
pip install -r requirements.txt
streamlit run app.py

🧾 requirements.txt

Your final minimal (correct) file:

streamlit
pandas
numpy
requests
urllib3




☁️ Deployment (Streamlit Cloud)

Push to GitHub

Go to https://streamlit.io/cloud

Deploy app → Select repo → Choose app.py

Done 🎉

No card required. Hosting is completely free.

🚀 Future Enhancements

Actor/Director search

Collaborative filtering model

Hybrid deep-learning embeddings

Watchlist system

Movie trailers integration

More TMDB metadata (budget, revenue, runtime, etc.)

👨‍💻 Developer

Yuvraj Lamba
Machine Learning & Frontend Developer
🚀 Passionate about AI, ML, React, and full-stack apps.

❤️ Credits

TMDB API

Kaggle TMDB 5000 Dataset

Streamlit

Scikit-Learn

