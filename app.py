import streamlit as st
import pickle
import pandas as pd
import requests
import json

temp = requests.post(
    "https://id.twitch.tv/oauth2/token?client_id=qojwjrgyeew7q2u5azazc3lewb97b5&client_secret"
    "=8v19y04bbxfanaozm8ycvwswuwa405&grant_type=client_credentials").json()
access_token = temp['access_token']

igdb_endpoint = 'https://api.igdb.com/v4/games'
igdb_headers = {
    'Client-ID': 'qojwjrgyeew7q2u5azazc3lewb97b5',
    'Authorization': f'Bearer {access_token}'
}


def get_cover_url(game_name):
    query_params = f'search "{game_name}"; fields cover.image_id;'
    alt_poster = 'https://static.displate.com/857x1200/displate/2022-04-15' \
                 '/7422bfe15b3ea7b5933dffd896e9c7f9_46003a1b7353dc7b5a02949bd074432a.jpg'
    try:
        response = requests.post(igdb_endpoint, headers=igdb_headers, data=query_params)
        game_data = json.loads(response.content.decode('utf-8'))
        cover_image_id = game_data[0]['cover']['image_id']
        cover_url = f'https://images.igdb.com/igdb/image/upload/t_cover_big/{cover_image_id}.jpg'
        return cover_url
    except:
        return alt_poster

def recommend_game(game):
    game_index = games[games['Name'] == game].index[0]
    distances = similarity[game_index]
    games_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: 6]

    recommended_games = []
    recommended_game_posters = []
    for i in games_list:
        recommended_games.append(games.iloc[i[0]]['Name'])
        recommended_game_posters.append(get_cover_url(games.iloc[i[0]]['Name']))
    return recommended_games, recommended_game_posters


games_dict = pickle.load(open('games_dict.pkl', 'rb'))
games = pd.DataFrame(games_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Game Recommender System')

selected_game_name = st.selectbox('Which game would like to search?', games['Name'].values)

if st.button('Recommend'):
    names, posters = recommend_game(selected_game_name)
    col = st.columns(5)
    for i in range(0, 5):
        with col[i]:
            st.text(names[i])
            st.image(posters[i])
