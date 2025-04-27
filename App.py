import streamlit as st
import pickle as pk
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

# Constants
FALLBACK_POSTER_URL = "https://via.placeholder.com/500x750?text=No+Image"

# CSS for background and footer
page_style = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #141E30, #243B55); 
    color: white;
}
[data-testid="stSidebar"] {
    background: #141E30;
    color: white;
}
footer {
    visibility: hidden;
}
footer:after {
    content:'© 2025 Movie Recommender | Created by Helpless';
    visibility: visible;
    display: block;
    text-align: center;
    padding: 5px;
    font-size: 12px;
    color: #FFFFFF;
    background-color: #141E30;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=349125f0d9c1b447f5cec267889240f1&language=en-US"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return FALLBACK_POSTER_URL
    except Exception as e:
        st.warning(f"Error fetching poster for movie ID {movie_id}: {e}")
        return FALLBACK_POSTER_URL

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Streamlit App
st.header('🎬 Movie Recommender System')

# Load movie data
movies = pk.load(open('movies.pkl', 'rb'))
similarity = pk.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a movie you like", movie_list)

if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):  # Spinner animation
        time.sleep(2)  # Simulate processing time
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in columns
    st.subheader("Top Recommendations:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx])
            st.caption(recommended_movie_names[idx])