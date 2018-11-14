# -*- coding: utf-8 -*-
"""
lesson5_rastertools.py

Function defining-harjoitus

Created on Wed Nov 14 10:25:44 2018

@author: Suvi Hatunen
"""
import numpy as np
import json

def normalize(array):
    """Normalizes numpy arrays into scale 0.0 - 1.0"""
    array_min, array_max = array.min(), array.max()
    return ((array-array_min)/(array_max-array_min))

def getFeatures(gdf):
    """
    Function to parse features 
    from GeoDataFrame in such a manner 
    that rasterio wants them
    """
    features = [json.loads(gdf.to_json())['features'][0]['geometry']]
    return features