# -*- coding: utf-8 -*-
"""
lesson2_map_projections.py

Tama skripti sialtaa luennon 2 harjoituksia aiheesta:
- koordinaattijarjestelmat

Created on Mon Nov 12 15:24:59 2018

@author: Suvi Hatunen
"""

import geopandas as gpd

# luetaan data
fp = "L2_data/Europe_borders.shp"
data = gpd.read_file(fp)

# tsekataan projektio
data.crs

# tehdaan kopio
geo = data.copy()

# Reproject the data
geo = geo.to_crs(epsg=3035)

import matplotlib.pyplot as plt

# Make subplots that are next to each other
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 8))

# Plot the data in WGS84 CRS
data.plot(ax=ax1, facecolor='gray');

# Add title
ax1.set_title("WGS84", fontsize=16);

# Plot the one with ETRS-LAEA projection
geo.plot(ax=ax2, facecolor='blue');

# Add title
ax2.set_title("ETRS Lambert Azimuthal Equal Area projection", fontsize=16);

# Remove empty white space around the plot
plt.tight_layout()

# save figure
plt.savefig("projection.png", dpi=300)

#saving to shape
# Ouput filepath
outfp = "L2_data/Europe_borders_epsg3035.shp"

# Save to disk
geo.to_file(outfp)

# fix the crs in windows (menee tallennuksessa hukkaan)
# ei toimi talla koneella viela
import pycrs

geo.crs = pycrs.parser.from_epsg_code(3035).to_proj4()

# save again
geo.to_file(outfp)
