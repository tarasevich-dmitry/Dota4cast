import streamlit as st
import pandas as pd
import numpy as np
import time
import webbrowser
from PIL import Image
import trueskill
from math import sqrt, log, log2
from trueskill import BETA
from trueskill.backends import cdf
import io

#Here used unsafe function to set canonical url for google search, MAY BE REMOVED FROM STREAMLIT!!!
st.write('<link rel="canonical" href="http://www.dota4cast.ml/" />',unsafe_allow_html=True)


st.title('Dota4cast Beta')

st.write("""
**Dota4cast.ml is a machine learning based platform that is building Dota 2 largest library of analytical tools, odds predicting tools and data to make that information accessible and useful for all Dota players and researchers.**
""")

image = Image.open('main_img.jpg')
st.image(image, caption=' ', use_column_width=True)

"""
#  Welcome.

Year by year eSports betting is gaining popularity among bettors, and it is clear that bookmakers couldn’t stay aside from a such rapidly growing sports direction.

One of the main advantages of betteors is that bookmaker analysts usually find it more difficult to place quotes in the events of eSports. Accordingly, the gambler has more chances to beat the bookie, if he is well versed in the chosen eSports discipline. However, this naturally applies to more “non-specialized” bookmakers.
Another eSports benefit for bettors is that here team-outsiders win much more often than in other sports. Accordingly, it is quite difficult for bookmakers to predict these victories.

Our solution will bring your betting experience on a new level.


History of eSports online gambling market (in bln $):
"""

#From -  https://esportsentertainmentgroup.com/wp-content/uploads/2018/04/eSportsBetting-ThePastandFuturev3.pdf
df = pd.DataFrame({
  '2009': [24.73],
  '2010': [27.58],
  '2011': [30.27],
  '2012': [32.67],
  '2013': [35.52],
  '2014': [37.47],
  '2015': [41.36],
  '2016': [45.86],
  '2017': [50.65],
  '2018': [56.05]
})


#chechbox to show graphs
if st.checkbox('Show dataframe'):
#    chart_data = pd.DataFrame(
#       np.random.randn(20, 3),
#       columns=['a', 'b', 'c'])
    st.line_chart(df)


#Put mmr widgets in a sidebar
df_mmr = pd.DataFrame({
  'first column': [1, 2, 3, 4, 5, 6, 7, 8]
})

option = st.sidebar.selectbox(
    'How much mmr do you have?',
     df_mmr['first column'])

#appears on bottom:
#'You selected:', option

####################################################################################
###True Skill part

#Upload data
df2 = pd.read_csv("selected_team_matches.csv")
matches_info = pd.read_csv('selected_team_matches.csv').sort_values(['match_id'])

#Get all team names from df
#"""
#Check all available teams for analisys:
#"""
#st.write(matches_info.radiant.unique())

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
    #st.image(image_s, caption=' ', use_column_width=True)
    st.write('Contact us on e-mail: dota4cast@gmail.com')


#Put mdropdown menu wuth teams
df_teams = matches_info.radiant.unique()


option1 = st.selectbox(
    'Chouse team 1:',
     df_teams)

option2 = st.selectbox(
    'Chouse team 2:',
     df_teams)


st.write(option1,'**Win probability is:**', win_probability(Rates[option1], Rates[option2]))
#####################################################################################



###################################################################################
#map
"""

**Tier 1 Tournaments map**
"""

map_data=pd.read_csv('map_coords.csv')


# Adding code so we can have map default to the center of the data
midpoint = (np.average(map_data['latitude']), np.average(map_data['longitude']))

st.deck_gl_chart(
            viewport={
                'latitude': midpoint[0],
                'longitude':  midpoint[1],
                'zoom': 1
            },
            layers=[{
                'type': 'ScatterplotLayer',
                'data': map_data,
                'radiusScale': 250,
   'radiusMinPixels': 4,
                'getFillColor': [248, 24, 148],
            }]
        )
"""
Tier 1 Tournaments is typically tournaments with an outstanding prize pool, as a rule played offline, and feature the best world teams. They are commonly held by well-established franchises or Valve, considered especially prestigious amongst the community.
"""
###################################################################################


if st.button('Contact us ٩(◕‿◕｡)۶'):
    #st.image(image_suck, caption=' ', use_column_width=True)
    st.write('dota4cast@gmail.com')

url_twitter = 'https://twitter.com/dota4cast'

if st.button('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ follow twitter'):
    webbrowser.open_new_tab(url_twitter)

"""
            *Copyright © 2020 dota4cast.ml All Rights Reserved. Dota 2 is a registered trademark of Valve Corporation. All game images and names are property of Valve Corporation.*
"""


#xD
st.balloons()



#df = pd.read_csv("data.csv")
#st.line_chart(df)

#Atl+shift+t to open terminal
#streamlit run main.py
