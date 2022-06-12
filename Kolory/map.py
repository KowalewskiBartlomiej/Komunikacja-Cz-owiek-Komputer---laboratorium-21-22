from os import close
from typing import Mapping
import numpy as np
import matplotlib.pyplot as plt

def loadfile(filename):
    file = open(filename, 'r')

    data = file.readlines()
    map_height, map_width, point_distance = [int(val) for val in data[0].split()]
    points = []
    for i in range(1, len(data)):
        points.append(list(map(float, data[i][:-2].split())))
    
    file.close()

    return map_height, map_width, point_distance, points

def hsv2rgb(h, s, v):
    if (s==0):
        return (v,v,v)
    h_i = np.floor(h*6)
    f = h*6 - h_i
    p = v * (1 - s)
    q = v * (1 - (s*f))
    t = v * (1 - (s * (1-f)))
    if (h_i==0 or h_i==6):
        return ((v,t,p))
    elif (h_i==1):
        return ((q,v,p))
    elif (h_i==2):
        return ((p,v,t))
    elif (h_i==3):
        return ((p,q,v))
    elif (h_i==4):
        return ((t,p,v))
    else:
        return ((v,p,q))

def gradient_hsv_unknown(h, s, v):
    return hsv2rgb(-1/3*h+1/3, s, v)

map_height, map_width, point_distance, points = loadfile('big.dem')

points = np.array(points)

normalized_points = (points - np.amin(points))/(np.amax(points)-np.amin(points))

color_points = np.zeros((map_height, map_width, 3))

for i in range(map_height):
    for j in range(map_width):
        saturation = 1
        value = 1
        if j > 0:
            dif = points[i, j]-points[i, j-1]
            dif = dif * 17 / (np.max(points))
            if dif > 0:
                value -= abs(dif)
            else:
                saturation -= abs(dif)
        color_points[i, j] = np.array(gradient_hsv_unknown(normalized_points[i, j], saturation, value))

fig, ax = plt.subplots()

ax.imshow(color_points)
plt.savefig('mapa.pdf')