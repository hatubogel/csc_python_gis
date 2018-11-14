# -*- coding: utf-8 -*-
"""
lesson4_nn.py

Tama skripti sisaltaa luennon4 harjoituksia
- lahimman naapurin analyysit

Created on Tue Nov 13 15:11:30 2018

@author: Suvi Hatunen
"""
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import geopandas as gpd

def nearest(row, geom_union, df2, geom1_col='geometry', geom2_col='geometry', ser_column=None):
    #alla fiksu tapa kommentoida def-funktioita, nakyy helpissa
    """
    Finds the closest point from the set of points.
    
    Parameters
    ----------
    
    geom_union: shapely.MultiPoint
    
    """
    # Find geometry that is closest
    nearest = df2[geom2_col] == nearest_points(row[geom1_col], geom_union)[1]
    
    # get the corresponding value from df2
    value = df2[nearest][ser_column].get_values()[0]
    
    return value

# datapolut
fp1 = 'L4_data/PKS_suuralue.kml'
fp2 = 'L4_data/addresses.shp'

# driverin aktivointi
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

# luetaan datat
polys = gpd.read_file(fp1, driver='KML')
src_points = gpd.read_file(fp2)

# unary union
unary_union = src_points.unary_union

# calculate centroif for the polygons
polys['centroid'] = polys.centroid

# find the nearest station for each polygon centroid
polys['nearest_id'] = polys.apply(nearest, geom_union=unary_union, df2=src_points, geom1_col='centroid', ser_column='id', axis=1)
