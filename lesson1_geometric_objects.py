# -*- coding: utf-8 -*-
"""
Kaikki materiaalit: https://automating-gis-processes.github.io/CSC/index.html

lesson1_geometric_objects.py

Tama skripti sisaltaa harjoituksia 1 oppitunnilta:
shapely geometric objetcs

Created on Mon Nov 12 10:58:46 2018

@author: Suvi Hatunen
"""

from shapely.geometry import Point, LineString, Polygon

# Point objetcs
#------

#create point geometric objects with coordinates
point1 = Point(2.2, 4.2)
point2 = Point(7.2, -25.1)
point3 = Point(9.26, -2.456)
point3D = Point(9.26, -2.456, 0.57)

#point type
point_type = type(point1)

#get the coordinates
point_coords = point1.coords

#get xy coordinates
xy = point1.xy
print(xy)

#get x and y coordinates
x = point1.x
y = point1.y

# calculate distance between point1 and point2
point_dist = point1.distance(point2)
print(point_dist)

#create a buffer with distance of 20 units
point_buffer = point1.buffer(20)


# LineString objects
#----------

#create line based on shapely points
line = LineString([point1, point2, point3])

#create line based on coordinate tuples
line2 = LineString([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

#coordinates
linexy = line.xy

#get x and y coordinates
lx = line.xy[0]
ly = line.xy[1]

#lenght of the line
l_length = line.length

#cetroid of the line
l_centroid = line.centroid

#type of the centroid
cent_type = type(l_centroid)


# Polygon objetcs
#-----------------

#create polygon
poly = Polygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)]) #coordinatetuples

point_list = [point1, point2, point3]
poly2 = Polygon([(p.x, p.y) for p in point_list]) #points

#get geometry type as string
poly_type = poly.geom_type

# calculate area
poly_area = poly.area

#centroid
poly_cent = poly.centroid

#bounding box
poly_bbx = poly.bounds

#create bounding box geometry
from shapely.geometry import box
bbox = box(*poly_bbx) #vaatii asterixin, jotta purkaa bounding box coordinates

# get exterior
poly_ext = poly.exterior

# exterior type is LinearRing
type_ext = type(poly_ext)

# legth of ecterior
poly_ext_length = poly.exterior.length

# Polygon with hole
world_exterior = [(-180, 90), (-180, -90), (180, -90), (180, 90)] #ymparyspolygoni
hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]] #reian koordinatit

#ensin ulkokuoren luonti
world = Polygon(shell=world_exterior)

#sitten lisataan reika
world_has_a_hole = Polygon(shell=world_exterior, holes=hole)

#sama toimii myos nain, eli ilman noita maarityksia shell ja holes
world_has_a_hole2 = Polygon(world_exterior, hole)





