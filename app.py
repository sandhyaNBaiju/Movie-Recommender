import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
import os

def download_file(url, filename):
    if not os.path.exists(filename):
        with st.spinner("Downloading similarity file..."):
            response = requests.get(url)
            with open(filename, "wb") as f:
                f.write(response.content)

# ✅ your correct direct link
file_url = "https://drive.google.com/uc?id=1bgxw1aD7--vFp22TGo2lSPOJ4ziuJVia"

download_file(file_url, "similarity.pkl")

# ✅ check BEFORE loading
if not os.path.exists("similarity.pkl"):
    st.error("similarity.pkl not found! Check your download link.")
    st.stop()

similarity = pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=fbe09f307eb7d7726b2e5f4dffe88edf".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie_name):
    movies_index = movies[movies['title'] == movie_name].index[0]
    distance = similarity[movies_index]
    movie_list = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies =[]
    recommended_movies_posters = []
    for movie in movie_list:
        movies_id = movies.iloc[movie[0]].Movie_id_x

        recommended_movies.append(movies.iloc[movie[0]]['title'])
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies_id))
    return recommended_movies, recommended_movies_posters

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

# similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Movies List",
    movies_list)

if st.button("Recommend", type="primary"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[3])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


