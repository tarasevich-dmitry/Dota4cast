import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import trueskill
from math import sqrt, log, log2
from trueskill import BETA
from trueskill.backends import cdf
import io


st.title('Dota4cast v.0.3')

st.write("""
Dota4cast is the key to protect gamblers and improve integrity
""")


image = Image.open('main_img.jpeg')
st.image(image, caption=' ', use_column_width=True)

"""
#  Welcome, bettor.

Year by year eSports betting is gaining popularity among bettors, and it is clear that bookmakers couldn’t stay aside from a such rapidly growing sports direction.

One of the main advantages of betteors is that bookmaker analysts usually find it more difficult to place quotes in the events of eSports. Accordingly, the gambler has more chances to beat the bookie, if he is well versed in the chosen eSports discipline. However, this naturally applies to more “non-specialized” bookmakers.
Another eSports benefit for bettors is that here team-outsiders win much more often than in other sports. Accordingly, it is quite difficult for bookmakers to predict these victories.

Our solution will bring your betting experience on a new level, removing randomness from it.


History of eSports online gambling market (in bln $):
"""
#From -  https://esportsentertainmentgroup.com/wp-content/uploads/2018/04/eSportsBetting-ThePastandFuturev3.pdf

# Any time that Streamlit sees a variable or a liter    al value on its own line, it automatically writes that to your app using st.write().
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

df
#chechbox to show
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)


"""
Zhytomyr Dota users
"""
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [50.25, 28.7],
    columns=['lat', 'lon'])

st.map(map_data)

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
"""
Check all available teams for analisys:
"""
st.write(matches_info.radiant.unique())

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


#Rates['VP 2']

def win_probability(player_rating, opponent_rating):
    delta_mu = player_rating.mu - opponent_rating.mu
    denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
    return cdf(delta_mu / denom)


"""
Vp Win probability:
"""

st.write(win_probability(Rates['VP 2'], Rates['EG']))



"""
            ©2020 Dota4cast.com
            All rights reserved
"""
#df = pd.read_csv("data.csv")
#st.line_chart(df)



#Atl+shift+t to open terminal
