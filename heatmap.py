# -*- coding: utf-8 -*-
"""
Created on Tue May 16 11:17:23 2023

@author: janhr
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
from geotext import GeoText


data = pd.read_excel('Bili.xlsx')

#extracting the countries:
data['country'] = data['birth_place'].apply(lambda x: GeoText(x).countries[0] if GeoText(x).countries else None)

#print(data)
#data.to_excel('countries_as.xlsx')

#so that the net_worth column contains only numerical values:
data['net_worth'] = data['net_worth'].str.replace('$', '').str.replace(' Billion', '').astype(float)

#print(data['net_worth'])

#group the data by country+ calculate the total net worth for each country:
grouped_data = data.groupby('country')['net_worth'].sum().reset_index()

#print(grouped_data)

#mapping country names to match the naturalearth_lowres dataset:
country_name_map = {
    'United States': 'United States of America',
    'Czech Republic': 'Czechia'
}

grouped_data['country'] = grouped_data['country'].map(country_name_map).fillna(grouped_data['country'])


#loading the world map shapefile:
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#print(world['name'])

#merging the data with the world map based on the country name:
merged_data = world.merge(grouped_data, left_on='name', right_on='country', how='left')

#print(merged_data)

#filling Nan values with 0:
merged_data['net_worth'] = merged_data['net_worth'].fillna(0)
#♥print(merged_data)

fig = px.choropleth(
    merged_data,
    locations='iso_a3',
    color='net_worth',
    hover_name='name',
    projection='natural earth',
    color_continuous_scale='amp',
    range_color=(0, merged_data['net_worth'].max()),  #setting the range of the color scale
)

#print(fig)

fig.update_geos(showcountries=True, countrycolor='gray', showcoastlines=True, coastlinecolor='gray')

#print(fig)
#show the heatmap:
fig.show()
