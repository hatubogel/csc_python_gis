# -*- coding: utf-8 -*-
"""
lesson2_geopandas.py

Tama skripti sisaltaa toisen oppitunnin harjoituksia:
- spatilaalisen datan kirjoitus ja luku geopandas'in avulla

Created on Mon Nov 12 12:20:11 2018

@author: Suvi Hatunen
"""

import geopandas as gpd

#set filepath
fp = "L2_data\\DAMSELFISH_distributions.shp"

#read the file with geopandas
data = gpd.read_file(fp)

# type of the data
type(data)

# first two rows of the data
print(data.head(2))

# print column names of the geodataframe
cols = data.columns

# plot the geometry
data.plot()

# create output path for the data
outfp = "L2_data/DAMSELFISH_distributions_SELECTION.shp"

# select first 50 rows
selection = data[0:50]

# write selection into a new shapefile
selection.to_file(outfp)

# tuettuja tiedostomuotoja
# ei sisalla kaikkia
import fiona
fiona.supported_drivers

# tietyn sarakkeen tiedot, tassa tapauksessa kentta geometry
print (data['geometry'].head())

# jos valinta halutaan tehda jonkun tietyn parametrin mukaan
#tehdaan valinta
sel3 = data[['geometry', 'BINOMIAL']]
#uniikit lajit poimitaan kentasta
unique = data['BINOMIAL'].unique()
#valinta tehdaan
criteria = 'Stegastes redemptus'
fish_a = data.loc[data['BINOMIAL'] ==criteria]
#pseudoa: muuttuja = data.loc[data['VALUE1']>0 &  data['VALUE2']<100]

#shapely-funktioita voi kayttaa myos nailla shape-datoilla
# valitaan 5 ekaa rivia
selection = data[0:5]

# iteroidaan rivien lapi
for index, row in selection.iterrows(): #iterrows on vahan niinkuin cursori arcpyssa
    poly_area = row['geometry'].area  #hae ala
    print("Polygon area at index {index} is: {area:.3f}".format(index=index, area=poly_area))

# tehdaan kentta jonka nimi on area
data['area'] = data.area
data['centroid'] = data.centroid

#kenttein sisallon tayttoa?
# ilmeisesti saman asian voi tehda myos kahdella muulla tapaa
data['area1'] = data.apply(lambda row: row['geometry'].area, axis=1)# lasketaan riveittain asioita kun axis = 1
def calc_area(row):
    return row['geometry'].area
data['area2'] = data.apply(calc_area, axis=1)

# printataan pari ekaa rivia
print(data['area'].head(2))

# voidaan tutkia myos max, min ja keskiarvo pinta-alat
max_area = data['area'].max()
min_area = data['area'].min()
mean_area = data['area'].mean()

# otetaan kopio ja muutetaan geometria centroidiksi ja tallennetaan uudeksi shapeksi
geo = data.copy()
geo = geo.set_geometry('centroid') #aktiivinen geometria-kentta
geo = geo.drop('geometry', axis=1) #shapessa voi olla vain yhden sortin geometriaa, pitaa poistaa ylimaaraiset ennen tallennusa
geo.to_file('geom_centroids.shp')

# ja printataan kyseiset arvot
print("Max area: {max}\nMin area: {min}\nMean area: {mean}".format(max=round(max_area, 2), min=round(min_area, 2), mean=round(mean_area, 2)))    

# calculater in (geo)DataFrame
geo['areaX2'] = geo['area'] *2

# luodaan uusi tyhja geometria dataan
from shapely.geometry import Point, Polygon #importoidaan tarvittavat moduulit

newdata = gpd.GeoDataFrame()

# luodaan kentta geometry
newdata['geometry'] = None

# lisataan uuteen dataan senaatintori
coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly5 = Polygon(coordinates) #shapely-objekti
newdata.loc[0, 'geometry'] = poly5 #tungetaan indeksiin 0

# lisataan kentta location
newdata.loc[0, 'location'] = 'Senaatintori'

# saving multiple shape-files JAI KESKEN
grouped = data.groupby('BINOMIAL')

for key, values in grouped:
    individual_fish = values

print('Key:', key)
print(individual_fish)
