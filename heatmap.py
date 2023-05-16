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

# Group the data by country and calculate the total net worth for each country
grouped_data = data.groupby('country')['net_worth'].sum().reset_index()

#print(grouped_data)

# Load the world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#print(world['name'])

# Merge the data with the world map based on the country name
merged_data = world.merge(grouped_data, left_on='name', right_on='country', how='left')

#print(merged_data)

# Fill NaN values with a default value (e.g., 0):
merged_data['net_worth'] = merged_data['net_worth'].fillna(0)
#♥print(merged_data)

# Plot the heatmap using Plotly
fig = px.choropleth(merged_data, locations='iso_a3', color='net_worth',
                    hover_name='name', projection='natural earth')

#print(fig)

fig.update_geos(showcountries=True, countrycolor='gray', showcoastlines=True, coastlinecolor='gray')

#print(fig)
# Show the heatmap
fig.show()
