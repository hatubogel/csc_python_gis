# -*- coding: utf-8 -*-
"""
lesson3_osm_data.py

Tama skripti sisaltaa luento3 harjoitukset:
- opsen street mapin kasittely

Created on Tue Nov 13 11:18:02 2018

@author: Suvi Hatunen
"""
import osmnx as ox
import matplotlib.pyplot as plt

# specify the name of the AOI
place_name = "Kamppi, Helsinki, Finland"

# fetch osm street network from Kamppi
graph = ox.graph_from_address(place_name)

# plot the streets
fig, ax = ox.plot_graph(graph)

# convert the graph to geodataframes
nodes, edges = ox.graph_to_gdfs(graph)

# retrieve buildings from Kamppi
buildings = ox.buildings_from_address(place_name, distance=1000)

# footprint of Kamppi
footprint = ox.gdf_from_place(place_name)

# retrieve POI from osm
restaurants = ox.pois_from_place(place_name, amenities=['restaurant', 'bar'])

# plot everything together
# at the bottom the footprint
ax = footprint.plot(facecolor='black')
# the next layer is street edges
ax = edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')
# the next one is buildings, alpa tarkoittaa transparenttiutta 0= transparent, 1=non-transparent
ax = buildings.plot(ax=ax, facecolor='khaki', alpha=0.7)
# on the top the restaurants
ax = restaurants.plot(ax=ax, color='green', alpha=0.7, markersize=10)
