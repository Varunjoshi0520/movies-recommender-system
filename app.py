import pandas as pd
import pickle
import streamlit as st
import requests


# TMDB API KEY
API_KEY = "886149918fa0b53625066f77a38f0fe9"

NO_POSTER = "https://via.placeholder.com/300x450?text=No+Poster"


# Fetch Poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    for _ in range(3):
        try:
            response = requests.get(url, timeout=20)

            if response.status_code == 200:
                data = response.json()

                if data.get("poster_path"):
                    return (
                        "https://image.tmdb.org/t/p/w500"
                        + data["poster_path"]
                    )
        except:
            pass

    return NO_POSTER


def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movie_names, recommended_movie_posters

movies_dict = pickle.load(
    open("movie_dict.pkl", "rb")
)

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(
    open("similarity.pkl", "rb")
)

movie_list = movies["title"].values


# Streamlit UI
st.header("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])