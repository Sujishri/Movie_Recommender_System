import streamlit as st
import pickle
import requests
import os

# Load data once and cache
@st.cache_data
def load_data():
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    return movies, similarity

movies, similarity = load_data()
movies_list = movies['title'].values  # For dropdown

# Function to download a single poster based on movie title and id
def download_poster(movie_title, movie_id):
    file_path = f"posters/{movie_id}.jpg"
    if not os.path.exists(file_path):
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey=25a7a02b"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_url = data.get('Poster')
            if poster_url and poster_url != 'N/A':
                image_data = requests.get(poster_url).content
                with open(file_path, "wb") as file:
                    file.write(image_data)
                return file_path
    return file_path if os.path.exists(file_path) else "https://via.placeholder.com/500x750?text=No+Image"








# Movie recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movies = []
    recommend_posters = []
    for i in distances[1:6]:  # Get top 5 recommended movies
        movie_title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movie_title)
        poster_path = download_poster(movie_title, movie_id)
        recommend_posters.append(poster_path)
    return recommend_movies, recommend_posters

st.header("Movie Recommender System")



# User selects a movie
selectvalue = st.selectbox("Select a movie from the dropdown", movies_list)

# Show recommendations when button is clicked
if st.button("Show Recommendations"):
    movie_names, movie_posters = recommend(selectvalue)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(movie_names[i])
            st.image(movie_posters[i])