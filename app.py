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
    recommended_movies_links = []   # NEW

    for movie in movie_list:
        idx = movie[0]

        # 1. FIRST define title
        title = str(movies.iloc[idx]["title"]).strip()

        movies_id = movies.iloc[idx]["Movie_id_x"]

        recommended_movies.append(movies.iloc[movie[0]]['title'])
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies_id))

        # imdb link
        imdb_url = "https://www.imdb.com/find?q=" + title.replace(" ", "+")
        recommended_movies_links.append(imdb_url)


    return recommended_movies, recommended_movies_posters, recommended_movies_links

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

# similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Movies List",
    movies_list)

if st.button("Recommend", type = "primary"):
    names, posters, links = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(
                f"""
                <a href="{links[i]}" target="_blank">
                    <img src="{posters[i]}" style="width:150px; border-radius:10px;">
                </a>
                """,
                unsafe_allow_html=True
            )
            st.write(names[i])
