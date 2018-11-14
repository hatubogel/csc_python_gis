# -*- coding: utf-8 -*-
"""
lesson5_raster_processing3.py

Tama skripti sisaltaa luennon5 raster processing harjoituksia
- mosaikointi
- zonal stats

Created on Wed Nov 14 13:12:53 2018

@author: Suvi Hatunen3
"""
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os
import pycrs
import matplotlib.pyplot as plt
from rasterstats import zonal_stats
import osmnx as ox
import geopandas as gpd

# Mosaikointi
#------------

dir_path = r'C:\IntroGIS_Suvi\L5_data'
out_fp = os.path.join(dir_path, "Helsinki_DEM2x2m_Mosaic.tif")

# make a search criteria to select DEM files
search_criteria = "L*.tif"
q = os.path.join(dir_path, search_criteria)

# glob function can be used to lista files from a dir with spwsific criteria
dem_fps = glob.glob(q) 

# open the source files
src_files_to_mosaic = [rasterio.open(fp) for fp in dem_fps]

# merge individual dems in array
mosaic, out_trans = merge(src_files_to_mosaic)

# plot the data
show(mosaic, cmap='terrain')

# copy and update the metadata
out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({ "driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,     
                 "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "
        }
        )

# write the final output in hard drive
with rasterio.open(out_fp, 'w', **out_meta) as dest:
    dest.write(mosaic)
    
# plot
#m = rasterio.open(out_fp)
#plt.imshow(m.read(1), cmap='terrain')
#plt.colorbar()
    
    
# Zonal statistics
#-----------------

# read data
dem = rasterio.open(out_fp)

# keywords for kallio and pihlis that can be found in open street map
kallio_q = "Kallio, Helsinki, Finland"
pihlajamaki_q = "Pihlajamäki, Malmi, Helsinki, Finland"

# retrieve data using osmnx
kallio = ox.gdf_from_place(kallio_q)
pihlajamaki = ox.gdf_from_place(pihlajamaki_q)

# test that crs is same
#assert kallio.crs == dem.crs, "ei mätsää kalliossa"
#assert pihlajamaki.crs == dem.crs, "ei mätsääpihliksessa"

# reproject to same crs as dem
kallio = kallio.to_crs(crs="+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs ")
pihlajamaki = pihlajamaki.to_crs(crs="+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs ")

# plot the polygons on top of the dem
ax = kallio.plot(facecolor='None', edgecolor='red', linewidth=2)
ax = pihlajamaki.plot(ax=ax, facecolor='None', edgecolor='blue', linewidth=2)

# plot the dem
show((dem, 1), ax=ax)

# define wich one is higher
# read the dem values to array
array = dem.read(1)
# get the affine
affine = dem.transform

# calculate zonal stats for Kallio
zs_kallio = zonal_stats(kallio, array, affine=affine, stats=['min', 'max', 'mean', 'median', 'majority'])
# do the same to pihlajamaki
zs_pihlajamaki = zonal_stats(pihlajamaki, array, affine=affine, stats=['min', 'max', 'mean', 'median', 'majority'])

print(zs_kallio)
print(zs_pihlajamaki)

# which one is higher eli kuinka viitat listan sisalla olevaan dictionaryyn
if zs_kallio[0]['majority'] > zs_pihlajamaki[0]['majority']:
    print("kallio on korkeammalla")
else:
    print("pihlis on korkeammalla")

# useammalle kanavalle voi iteroita talla tavalla
#for channel in range(1,5):
#    zs_results[channel] = zonal_stats(polygon, channel_data_array, stats['min', 'max'])


