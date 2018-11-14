# -*- coding: utf-8 -*-
"""
lesson4_spatjoin.py

Tama skripti sisalta luennon4 harjoituksia
-spatial join

Created on Tue Nov 13 14:43:04 2018

@author: Suvi Hatunen
"""
import geopandas as gpd
import matplotlib.pyplot as plt

# luetaan datat
fp = 'L4_data/Vaestotietoruudukko_2015.shp'
pop = gpd.read_file(fp)
pointfp = 'L4_data/addresses.shp'
point = gpd.read_file(pointfp)

# ensure that the datasets are in same projection
point = point.to_crs(crs=pop.crs)

# do the crs match?
assert pop.crs == point.crs, "CRS does not match"

# make spatjoin
join = gpd.sjoin(point, pop, how="inner", op="within")

# visualize, pisteen symbolikoko verrannollinen kentan ASUKKAAT osuuteen kok.asukasmaaraan
join.plot(column='ASUKKAITA', cmap='Reds', markersize=join['ASUKKAITA']/1642*100)
