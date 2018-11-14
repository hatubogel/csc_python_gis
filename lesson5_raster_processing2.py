# -*- coding: utf-8 -*-
"""
lesson5_raster_processing2.py

Tama skripti sisaltaa luennon5 raster processing harjoituksia
-maskaus/klippaus
-ndvi-laskenta

Created on Wed Nov 14 11:06:45 2018

@author: Suvi Hatunen
"""
import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs
import os
import numpy as np
import matplotlib.pyplot as plt
from lesson5_rastertools import getFeatures

# datadir
data_dir = r"C:\IntroGIS_Suvi\L5_data"

# Masking the data
#-----------------

# input raster
fp = os.path.join(data_dir, "p188r018_7t20020529_z34__LV-FIN.tif")

# output raster
out_tif = os.path.join(data_dir, "Helsinki_Masked.tif")

# read the data
raster = rasterio.open(fp)

# visualize the NIR band (4 band)
show((raster, 4), cmap='terrain')

# WGS84 bounding box for the mask
minx, miny = 24.60, 60.00
maxx, maxy = 25.22, 60.35
bbox = box(minx, miny, maxx, maxy)
# create GeoDataFrame from the bounding box
crs_code = pycrs.parser.from_epsg_code(4326).to_proj4()
geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=crs_code)
print(geo)

# project the polygon into same crs as image
geo = geo.to_crs(crs=raster.crs)

# convert GeoDataFrame to geometric features dictionary
coords = getFeatures(geo)

# clip the raster with polyg
out_img, out_transform = mask(dataset=raster, shapes=coords, crop=1)

# copy the metadata from original
out_meta = raster.meta.copy()

# update the metadata, first parse epsg
epsg_code = int(raster.crs.data['init'].replace('epsg:',''))
epsg_proj4 = pycrs.parser.from_epsg_code(epsg_code).to_proj4()
out_meta.update({"driver": "GTiff",
                 "height": out_img.shape[1],
                 "width": out_img.shape[2],
                 "transform": out_transform,
                 "crs": epsg_proj4
                 }
                )

# tallennetaan rasteri
with rasterio.open(out_tif, "w", **out_meta) as dest:
    dest.write(out_img)

# plotataan rasteri
clippped = rasterio.open(out_tif)
show((clippped, 5), cmap='terrain')

# Raster map algebra: calculating NDVI
#-------------------

#luetaan datat
fp1 = out_tif
raster1 = rasterio.open(fp1)

# read red and nir channels
reed = raster1.read(3)
niir = raster1.read(4)

# calculate some stats to check the data and visualize
print(reed.mean())
print(niir.mean())
print(type(niir))
show(niir, cmap='terrain')

# convert integers to floats
reed = reed.astype('f4')
niir = niir.astype('f4')

# change numpy to allow dividing by zero
np.seterr(divide='ignore', invalid='ignore')

# calculate NDVI using numpy arrays
ndvi = (niir - reed)/(niir + reed)

# plotting the NDVI
plt.imshow(ndvi, cmap='terrain_r')
# add colorbar
plt.colorbar()














