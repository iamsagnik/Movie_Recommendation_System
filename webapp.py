import streamlit as st
import pickle
import pandas as pd 
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  dist = similarity[movie_index]
  movie_list = sorted(list(enumerate(dist)), reverse = True , key = lambda x:x[1])[1:6]
  recommended_movies_names = []
  recommended_movie_posters = []
  for i in movie_list:
    movie_id = movies.iloc[i[0]].movie_id
    recommended_movie_posters.append(fetch_poster(movie_id))
    recommended_movies_names.append(movies.iloc[i[0]].title)
  return recommended_movies_names,recommended_movie_posters 

similarity = pickle.load(open('similarity.pkl' , 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl' , 'rb'))
movies = pd.DataFrame(movies_dict)

st.header('Movie Recommendation System')

options = st.selectbox(
    "What would you like to see next?",
    movies['title'].values,
    index=None,
    placeholder="Type your movie name...",
)

st.markdown(
    """
    <style>
    .custom-font {
        font-family: 'Arial';
        font-size: 18px;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if st.button("Recommend"):
    if(options == None):
       st.write("Please select a option.")
    recommended_movie_names,recommended_movie_posters = recommend(options)
    col1,spacer, col2,spacer, col3 = st.columns([1, 0.1, 1, 0.1, 1])
    with col1:
        st.image(recommended_movie_posters[0])
        st.markdown(f"<p class='custom-font'>{recommended_movie_names[0]}</p>", unsafe_allow_html=True)        
        st.image(recommended_movie_posters[3])
        st.markdown(f"<p class='custom-font'>{recommended_movie_names[3]}</p>", unsafe_allow_html=True)            
    with col2:
        st.image(recommended_movie_posters[1])
        st.markdown(f"<p class='custom-font'>{recommended_movie_names[1]}</p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[4])
        st.markdown(f"<p class='custom-font'>{recommended_movie_names[4]}</p>", unsafe_allow_html=True)
    with col3:
        st.image(recommended_movie_posters[2])  
        st.markdown(f"<p class='custom-font'>{recommended_movie_names[2]}</p>", unsafe_allow_html=True)