# -*- coding: utf-8 -*-
"""
lesson5_raster_processing1.py

Tama skripti sisaltaa luennon5 harjoituksia
- rasteridatan lukeminen
- visuaalisointi

Created on Wed Nov 14 09:03:45 2018

@author: Suvi Hatunen
"""
import rasterio
import os
import numpy as np

# reading data
#-------------

# data directory, r korvaa kaksoiskenot
data_dir = r"C:\IntroGIS_Suvi\L5_data"
fp = os.path.join(data_dir, "Helsinki_masked_p188r018_7t20020529_z34__LV-FIN.tif")

# open the file
raster = rasterio.open(fp)

# raster metadata:
# Affine transform (how raster is scaled, rotated, skewed, and/or translated)
raster.transform
# dimensions
print(raster.width)
print(raster.height)
# number of bands
raster.count
# bounds of the file
raster.bounds
# raster driver = dataformaatti
raster.driver
# nodata-values for all channels
raster.nodatavals
# all above metadata plus some more
raster.meta

# read the data values to python
#------------------------------

# read band nro 1
band1 = raster.read(1)

# read all bands (tulee numpy-array)
array = raster.read()

# calculate stats for each band
stats = []
for band in array:
    stats.append({
            'min': band.min(),
            'mean': band.mean(),
            'median': np.median(band),
            'max': band.max()})
    
## calculate stats for each band, vaihtoehtoinen versio
#stats = []
#for idx, band in enumerate(array):
## enumerate tekee automaattisen laskurin, tjsp
#    band_stat = {
#            'min': band.min(),
#            'mean': band.mean(),
#            'median': np.median(band),
#            'max': band.max()
#            }
#    channel_stat = {'channel %s' % (idx+1): band_stat}
#    stats.append(channel_stat)
    
# show stats for each band
stats

 # visualizing data
 #------------------
 # importoidaan lisaa paketteja
from rasterio.plot import show
from rasterio.plot import show_hist
import matplotlib.pyplot as plt
from lesson5_rastertools import normalize #itse tehdyn funktion importtaus

# tassa valissa voisi lukea rasterin uudelleen, jos olisi uusi skripti

# piirretaan kanava 1
show((raster, 1))

# piirretaan kanava 3 eri tavalla
show(raster.read(3))

# piirretaan kaikki kanavat rinnakkain
# initialize subplots
# sharey tarkoittaa ettei jokaiselle tarvitse maaritella omia akseletia, vaan voidaan jakaa y-akseli ekan kanssa
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(10, 4), sharey=True)
# plot RGB
show((raster, 3), cmap='Reds', ax=ax1)
show((raster, 2), cmap='Greens', ax=ax2)
show((raster, 1), cmap='Blues', ax=ax3)
# add titles
ax1.set_title("Red")
ax2.set_title("Green")
ax3.set_title("Blue")

# RGB True color composite
# read bands into numpy-arrays
red = raster.read(3)
green = raster.read(2)
blue = raster.read(1)
# normalize the bands
redn = normalize(red)
greenn = normalize(green)
bluen = normalize(blue)  

# printataan kanavien normalisoidut arvot
#print("Normalized bands")
#print(redn.min(), '-', redn.max(), 'mean:', redn.mean())
#print(greenn.min(), '-', greenn.max(), 'mean:', greenn.mean())
#print(bluen.min(), '-', bluen.max(), 'mean:', bluen.mean())

# create rgb natural color composite
rgb = np.dstack((redn, greenn, bluen))
# plot teh composite
plt.imshow(rgb)
    
# False color composite goes similarly   

# Histogram of the data #JOKU MENI VIKAAN
show_hist(raster, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histogram")
    

