#This script parse tournaments location data from liquidepiad.org
#And convers it latitude\longitude. 
#It may run for 1-2 min, need to change geopandas to Google API to improve, TBD

import pandas as pd
import geopandas
import geopy
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from bs4 import BeautifulSoup
from urllib.request import urlopen

locator = Nominatim(user_agent="username")

url = "https://liquipedia.net/dota2/Tier_1_Tournaments"
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')


mydivs = soup.findAll("div", {"class": "divCell EventDetails Location Header"})

locations = []

for res in mydivs:
    one_loc=res.text
    locations.append(one_loc)


df=pd.DataFrame(locations)

df.columns = ['city_country']

#Remove tournaments with no specific location
new_df = df[(df.city_country != " Europe & CIS") & (df.city_country != " World") & (df.city_country != " Europe")] 



# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1/20)
# 2 - create location column
new_df['location'] = new_df['city_country'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
new_df['point'] = new_df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

new1_df = new_df.dropna()
df1=new1_df.reset_index(drop=True)


# 4 - split point column into latitude, longitude and altitude columns
df1[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df1['point'].tolist(), index=df1.index) 


df_final = df1[['latitude', 'longitude']].copy()

df_final.to_csv('map_coords.csv', index=False)
