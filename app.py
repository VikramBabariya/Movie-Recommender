import streamlit as st
import pandas as pd
import pickle
import requests


def get_poster_path(mov_id):
    data = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=29b9d4340834a4e239386d1fd0cced17&language=en-US'.format(mov_id)).json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    ind = movies[movies['title'] == movie].index[0]
    sims = similarity[ind]
    mov_list = sorted(list(enumerate(sims)), reverse=True, key=lambda x:x[1])[1:6]

    rec_list = []
    poster_path = []
    for i in mov_list:
        mov_id = movies.iloc[i[0]]['movie_id']
        rec_list.append(movies.iloc[i[0]]['title'])
        poster_path.append(get_poster_path(mov_id))
    return rec_list, poster_path


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Select Movie',
    movies['title'])

if st.button('Recommend'):
    rec_list, poster_list = recommend(selected_movie)

    n = len(rec_list)
    cols = st.columns(n)
    for i in range(n):
        with cols[i]:
            st.text(rec_list[i])
            st.image(poster_list[i])


