# -*- coding: utf-8 -*-
"""
lesson6_cloud_optimized_data.py

Talla skiprilla voi lukea pilvesta dataa

Created on Wed Nov 14 14:38:20 2018

@author: Suvi Hatunen
"""
import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Specify the path for Landsat TIF on AWS
fp = 'http://landsat-pds.s3.amazonaws.com/c1/L8/042/034/LC08_L1TP_042034_20170616_20170629_01_T1/LC08_L1TP_042034_20170616_20170629_01_T1_B4.TIF'

## See the profile
#with rasterio.open(fp) as src:
#    print(src.profile)

# get the profile
src = rasterio.open(fp)

# list the overviews    
oviews = src.overviews(1)
oview = oviews[-1]

# get the thumbnail
thumbnail = src.read(1, out_shape=(1, int(src.height // oview), int(src.width // oview)))

# plot
show(thumbnail, cmap='terrain')

# retrieve window (a subset) from full resolution raster
window = rasterio.windows.Window(1024, 1024, 1280, 2560)

#  retrieve the actual subset
subset = src.read(1, window=window)

# plotataan
show(subset, cmap='terrain')

# corine-dataa csc:n serverilla
fp2 = 'http://86.50.168.160/syke/corine/2012/corine_2012_0_6800000.tif'

src2 = rasterio.open(fp2)

oviews = src2.overviews(1)
oview = oviews[2]

thumbnail2 = src2.read(1, out_shape=(1, int(src2.height // oview), int(src2.width // oview)))

show(thumbnail2, cmap='Spectral')
