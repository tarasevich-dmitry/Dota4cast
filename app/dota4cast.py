# -*- coding: utf-8 -*-
# This demo lets you to explore dot4cast project, Dota 2 Esports analytics web app
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# More info: https://github.com/tarasevich-dmitry/Dota4cast
# Copyright 2021 dota4cast Inc.

import streamlit as st
from streamlit_disqus import st_disqus
import pandas as pd
import numpy as np
import time
import webbrowser
from PIL import Image
import trueskill
from math import sqrt, log, log2
from trueskill import BETA
from trueskill.backends import cdf
from joblib import dump, load
import pydeck as pdk
import io

def main():
    #Here used unsafe function to set canonical url for google search, MAY BE REMOVED FROM STREAMLIT!!!
    st.write('<link rel="canonical" href="http://www.dota4cast.ml/" />',unsafe_allow_html=True)

    #st.beta_set_page_config(page_title='Dota4cast')

    st.title('Dota4cast Beta')

    st.write("""
    **It is absolutely free and opensource project, check out source code [Github](https://github.com/tarasevich-dmitry/Dota4cast)**
    """)

    st.write("""
    **Dota4cast.ml is a machine learning based platform that is building Dota 2 analytical tools, odds prediction and gathering data to make that information accessible and useful for all Dota players and researchers.**
    """)

    #main front image
    image = Image.open('main_img.jpg')
    st.image(image, caption=' ', use_column_width=True)

    """
    #  Welcome.

    Year by year eSports betting is gaining popularity among bettors, and it is clear that bookmakers couldn’t stay aside from a such rapidly growing sports direction.

    One of the main advantages of betteors is that bookmaker analysts usually find it more difficult to place quotes in the events of eSports. Accordingly, the gambler has more chances to beat the bookie, if he is well versed in the chosen eSports discipline. However, this naturally applies to more “non-specialized” bookmakers.
    Another eSports benefit for bettors is that here team-outsiders win much more often than in other sports. Accordingly, it is quite difficult for bookmakers to predict these victories.

    Our solution will bring your betting experience on a new level.
    """

    #Put mmr widgets in a sidebar
    #df_mmr = pd.DataFrame({
    #  'first column': [1, 2, 3, 4, 5, 6, 7, 8]
    #})

    #option = st.sidebar.selectbox(
    #    'Chouse option what to do',
    #     df_mmr['first column'])


    #appears on bottom:
    #'You selected:', option

    ####################################################################################
    ###True Skill part

    #Upload data
    df2 = pd.read_csv("selected_team_matches.csv")
    matches_info = pd.read_csv('selected_team_matches.csv').sort_values(['match_id'])

    trueskill.setup(draw_probability=0)


    Rates = {}
    for index, row in matches_info.iterrows():
        team1 = row['radiant']
        team2 = row['dire']
        if team1 not in Rates:
            Rates[team1] = trueskill.Rating()
        if team2 not in Rates:
            Rates[team2] = trueskill.Rating()
        if row['winner'] == 'RADIANT':
            Rates[team1], Rates[team2] = trueskill.rate_1vs1(Rates[team1], Rates[team2])
        else:
            Rates[team2], Rates[team1] = trueskill.rate_1vs1(Rates[team2], Rates[team1])


    def win_probability(player_rating, opponent_rating):
        delta_mu = player_rating.mu - opponent_rating.mu
        denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
        return cdf(delta_mu / denom)


    if st.button('Check all available teams for analisys'):
        st.write(matches_info.radiant.unique())


    if st.button('Can`t find your team?'):
        st.write('Unfortunately some data can be outdated, we working on making data pipeline more reliable. Have suggestions? - Contact us on e-mail: dota4cast@gmail.com')

    #Put dropdown menu with teams
    df_teams = matches_info.radiant.unique()


    option1 = st.selectbox(
        'Chouse team 1:',
         df_teams)

    option2 = st.selectbox(
        'Chouse team 2:',
         df_teams)


    st.write(option1,'**Win probability is:**', win_probability(Rates[option1], Rates[option2]))
    #####################################################################################

    #map  TBD
    """
    **Tier 1 Tournaments map**
    """

    image2 = Image.open('map_tir1.png')
    st.image(image2, caption=' ', use_column_width=True)
    #map_data=pd.read_csv('map_coords.csv')

    # Adding code so we can have map default to the center of the data
    #midpoint = (np.average(map_data['latitude']), np.average(map_data['longitude']))


    #st.pydeck_chart(pdk.Deck(
    #    map_style='mapbox://styles/mapbox/light-v9',
    #    initial_view_state=pdk.ViewState(
    #        latitude=midpoint[0],
    #        longitude=midpoint[1],
    #        zoom=1,
    #        pitch=50,
    #    ),
    #    layers = pdk.Layer(
    #           'ScatterplotLayer',
    #           data=map_data,
    #           get_position='[lon, lat]',
    #           auto_highlight=True,
    #           radius=200,
    #           elevation_scale=4,
    #           elevation_range=[0, 1000],
    #           pickable=True,
    #           extruded=True,
    #        ),
    #))


    """
    Tier 1 Tournaments is typically tournaments with an outstanding prize pool, as a rule played offline, and feature the best world teams. They are commonly held by well-established franchises or Valve, considered especially prestigious amongst the community.
    """


    ###################################################################################
    #Wordcloud
    """
    **Dota 2 All Chat Wordcloud**
    """

    image_wc = Image.open('wc_dota.png')
    st.image(image_wc, caption=' ', use_column_width=True)

    """
    Dota 2 is notorious for having a somewhat toxic community. We construct a word cloud to inspect these claims and determine the frequency and flavour of the most common words. We get data from in-game all-chat.
    """

    ###################################################################################
    #Based on picks prediction TBD
    ###
#    """
#    **Pick win prediction:**
#    """

    #clf = load('f_model.joblib')
    #load hero list:
    #heroes=pd.read_csv('hero_names.txt')

    #df_heroes = heroes.Sven.unique()


    #col1, col2 = st.beta_columns(2)

    #ancient_1 = st.selectbox('1 radiant hero', df_heroes)
    #ancient_2 = st.selectbox('2 radiant hero', df_heroes)
    #ancient_3 = st.selectbox('3 radiant hero', df_heroes)
    #ancient_4 = st.selectbox('4 radiant hero', df_heroes)
    #ancient_5 = st.selectbox('5 radiant hero', df_heroes)

    #dire_1 = st.selectbox('1 dire hero', df_heroes)
    #dire_2 = st.selectbox('2 dire hero', df_heroes)
    #dire_3 = st.selectbox('3 dire hero', df_heroes)
    #dire_4 = st.selectbox('4 dire hero', df_heroes)
    #dire_5 = st.selectbox('5 dire hero', df_heroes)

    #st.write(option3,'**TEST:**')

    ###################################################################################
    if st.button('Source code (◕‿◕)♡'):
        st.write('https://github.com/tarasevich-dmitry/Dota4cast')

    if st.button('Contact us ٩(◕‿◕｡)۶'):
        st.write('dota4cast@gmail.com')

    url_twitter = 'https://twitter.com/dota4cast'

    if st.button('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ follow twitter'):
        st.write('https://twitter.com/dota4cast')
        #webbrowser.open_new_tab(url_twitter)


    st_disqus("streamlit-disqus-demo")

    """
                *Copyright © 2021 dota4cast.ml All Rights Reserved. Dota 2 is a registered trademark of Valve Corporation. All game images and names are property of Valve Corporation.*
    """

    #rofl ballons animation
    st.balloons()


if __name__ == "__main__":
    main()


#Atl+shift+t Atom sc
#To run app: streamlit run dota4cast.py
