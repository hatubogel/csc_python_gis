# -*- coding: utf-8 -*-
"""
lessons4_pointinpoly.py

Tama skripti sisaltaa luento4 harjoituksia
-point in polygon
-intersect

Created on Tue Nov 13 13:45:52 2018

@author: Suvi Hatunen
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.speedups

# kml driverin maarittelyt, ei ole automaattisesti kaytossa
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
# enabloidaan speedups
shapely.speedups.enable()

# read files
fp = 'L4_data/PKS_suuralue.kml'
polys = gpd.read_file(fp, driver='KML')
fpa = 'L4_data/addresses.shp'
data = gpd.read_file(fpa)

# select AOI
southern = polys.loc[polys['Name'] == 'Eteläinen']
# reset index ja droppaa vanha
southern = southern.reset_index(drop=1)

# conduct point in polygon query
# loc kohdistaa toimenpiteen indeksiin 0 ja kenttaan geometry
pip_mask = data.within(southern.loc[0, 'geometry'])
# select points that are wihtin Polygon
pip_data = data.loc[pip_mask]

#visualization JOKU MÄNI PIELEEN!!
ax = polys.plot(facecolor='gray')
ax = southern.plot(facecolor='red')
pip_data.plot(ax=ax, color='gold', markersize=2)
plt.tight_layout()