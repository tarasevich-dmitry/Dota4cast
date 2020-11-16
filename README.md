# Dota4cast
Dota 2 Esports analytics web app. Build with [Streamlit](https://www.streamlit.io/), deployed with [Heroku](https://www.heroku.com/)

Check it online www.dota4cast.ml

![Alt Text](https://github.com/tarasevich-dmitry/Dota4cast/blob/master/images/demo.gif)


<h3> Team winrate prediction: </h3>

  <summary>Predictions based on team previous results</summary>
 <br>
  
  Build on results of professional teams performance. 
  
--- 
<h4>Dota 2 word chat cloud</h4>

We construct a word cloud to determine the frequency and flavour of the most common words. We get data from in-game all-chat.

Run it online in [Google Colab](https://colab.research.google.com/drive/11bQpWGrzySjMsiIRCwkUPVzZUvMbkkN1?usp=sharing)

---
<h4>Dota Tir 1 Tournaments map</h4>

In tournaments_map`dota_map_parser.py` is a parser that takes data from [Liquipedia](https://liquipedia.net/dota2/Tier_1_Tournaments) using Beautifulsoup
and then geopy to translate locations to latitude & longitude, final map drawn in streamlit. 

---
<h4>Data</h4>

TBD

Initially data taken using [OpenDota](www.opendota.com) tools and API's

Aslo check out our [Twitter](twitter.com/dota4cast)


<h4>Credits</h4>

[Streamlit](https://github.com/streamlit/streamlit)

[Dotascience](https://github.com/dotascience/dotascience-hackathon)

[renanmav](https://www.kaggle.com/renanmav/dota-2-game-prediction)

