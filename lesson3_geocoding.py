# -*- coding: utf-8 -*-
"""
lesson3_geocoding.py

Tama skripti sisaltaa luennon3 harjoituksia:
- geocoding
- alussa vastauksia pyhiksen kysymyksiin

Created on Tue Nov 13 09:08:03 2018

@author: Suvi Hatunen
"""
#jaanne eiliselta:
#oikea koodi kaikkien exporttaus-formaattien loytamiseen
import fiona
from fiona._drivers import GDALEnv
env = GDALEnv()
env.start().drivers().keys()


#toinen jaanne eiliselta
#WFS-palvelujen lukeminen
import geopandas as gpd
import requests
import geojson 
import pycrs

# Specify the url for the backend
url = 'http://geo.stat.fi/geoserver/vaestoruutu/wfs'

#parametrit loytyy GetCapabilties-dokumentista
cab_params = dict(service='WFS', request='GetCapabilities')
cabap = requests.get(url, params=cab_params)
print(cabap.content)

# Specify parameters (read data in json format)
params = dict(service='WFS', version='2.0.0', request='GetFeature',
         typeName='vaestoruutu:vaki2017_5km', outputFormat='json')

# Fetch data from WFS using requests
r = requests.get(url, params=params)

# Create GeoDataFrame from geojson
dataX = gpd.GeoDataFrame.from_features(geojson.loads(r.content))

# Define CRS
#dataX.crs = {'init': 'epsg:3067'}
dataX.crs = pycrs.parser.from_epsg_code(3067).to_proj4()

# set geometry
dataX = dataX.set_geometry('geometry')

# remove column with list
dataX = dataX.drop('bbox', axis=1)

# save to disc
outfpX = "L2_data/Population_grid_5km.gpkg"
dataX.to_file(outfpX, driver="GPKG")

# paivan varsinainen sisalto alkaa tasta:
#------------------
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import geocode
import contextily as ctx #ei toimi

def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))
    return ax

# Filepath
fp = "L3_data/addresses.txt"

# Read the data, sep means separator
data = pd.read_csv(fp, sep=';')

# geocode addresses, provider on siis geokoodarin palveluntarjoaja
# nominatim on openstreetmapin palvelu
# user_agent tarkoittaa kayttaja-id:ta, keksi omasi
geo = geocode(data['addr'], provider='nominatim', user_agent='csc_user_sh')
geo.head()

# joinataan alkuperainen data geodoocattuun
# ei tarvita mitaan join-fieldia, silla datoje indeksi on automaattisesti sama
join = geo.join(data)
join.head()

# piirretaan data taustakartan paalle
#reprojisoidaan webmercatoriin
join = join.to_crs(epsg=3857)
ax = join.plot()
# lisataan taustakartta
add_basemap(ax=ax, zoom=12)

# Output file path
outfp = "L3_data/addresses.shp"

# Save to Shapefile
join.to_file(outfp)
