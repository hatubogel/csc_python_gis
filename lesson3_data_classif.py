# -*- c
"""
lesson3_data_classif.py

Tama skripti sisaltaa esimerkkeja luennon3 luokittelu ja visualisointikoodeista

Created on Tue Nov 13 13:08:17 2018

@author: Suvi Hatunen
"""
import geopandas as gpd
import pysal as ps
import matplotlib.pyplot as plt

#filepath
fp = "L3_data/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

#read the data
data = gpd.read_file(fp)

# exclude -1 values (NoData)
data = data.loc[data['pt_r_tt']>=0]

# plot 9 classes, myos enemman on mahdollista luokitella
# scheme joko equal_interval, quantiles tai fisher_jenkins
data.plot(column='pt_r_tt', scheme='Fisher_Jenks', k=9, cmap="RdYlBu", linewidth=0, legend=True)
plt.tight_layout()

#muiden luokittelijoiden  maarittely
# define the number of classes
k = 12

# initialize the natural breaks classifier
classifier = ps.Natural_Breaks.make(k=k)

# classify the travel time values
classifications = data[['pt_r_tt']].apply(classifier)

# rename the classified column into nb_pt_r_tt
# usemamma kentan nimeamisessa erota parit toisistaan pilkulla
classifications = classifications.rename(columns={'pt_r_tt':'nb_pt_r_tt'})

# conduct table join based on index
data = data.join(classifications)

# create a map based on new classes
ax = data.plot(column='nb_pt_r_tt', linewidth=0, legend=1)

# custom classifier
# create a custom classifier
class_bins = [10, 20, 30, 40 ,50, 60]
classifier = ps.User_Defined.make(class_bins)

custom_classifications = data[['pt_r_tt']].apply(classifier)

# rename the classified column into c_pt_r_tt
# usemamma kentan nimeamisessa erota parit toisistaan pilkulla
custom_classifications = custom_classifications.rename(columns={'pt_r_tt':'c_pt_r_tt'})

# conduct table join based on index
data = data.join(custom_classifications)

# plot distancemap
ax = data.plot(column='c_pt_r_tt', linewidth=0, legend=1)
