# -*- coding: utf-8 -*-
"""Predictions_OnTeam_Stage2_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aME6g2k-wkxO096cDcl_sa0xu3YSzj6t

**Prediction baced on team, used TrueSkill v1**
"""

!pip install trueskill

import pandas as pd
import trueskill

from math import sqrt, log, log2
from trueskill import BETA
from trueskill.backends import cdf

"""Upload data"""

from google.colab import files
uploaded = files.upload()

import io
df2 = pd.read_csv(io.BytesIO(uploaded['selected_team_matches.csv']))
# Dataset is now stored in a Pandas Dataframe

"""Downloading information about previous games and sorting it by Match_ID"""

matches_info = pd.read_csv('selected_team_matches.csv').sort_values(['match_id'])

"""Initialize the Trueskill parameters using the default parameters, except for the probability of a tied result, we have no draws in Dota 2"""

trueskill.setup(draw_probability=0)

"""Create a dictionary where we will store ratings. And we will train our system. For each match we will determine the winner and recalculate the ratings of the teams. If a team has not met before, we give it a default rating. In our simplest model, we take each team as an one virtual player."""

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

"""Now we can, for example, enjoy the rating of the Virtus.pro commers, which is hidden under the tag 'VP 2'"""

Rates['VP 2']

"""Let's try to evaluate the probability of winning Virtus.pro, for example, in a match with Evil Genius. Unfortunately in the trueskill library, there is no way to estimate the probability, but we know from the description that the ratings here are normally distributed. So let's make a function that will estimate the probability that the strength of the game of the first team will be greater than that of the second."""

def win_probability(player_rating, opponent_rating):
    delta_mu = player_rating.mu - opponent_rating.mu
    denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
    return cdf(delta_mu / denom)

"""Hooray, now we can evaluate the odds."""

win_probability(Rates['VP 2'], Rates['EG'])