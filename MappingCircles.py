from ZenithLocator import *
import numpy as np
import pandas as pd
from geopy.distance import Geodesic
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = "browser"

center_coords = zenith_locator(Jupiter)
center_lat = center_coords[0]
center_lon = center_coords[1]

earth_radius = 6371000  # in meters
distance_m = earth_radius * (np.pi / 2)
distance_m_div = distance_m / 9
bearings_deg = np.linspace(0, 360 - 360 / 720, 720)

def create_circle_coords(radius_deg, num_points=36):
    circle_points = []
    
    for i in range(num_points):
        bearing = i * (360 / num_points)
        
        result = Geodesic.WGS84.ArcDirect(center_lat, center_lon, bearing, radius_deg)
        
        circle_points.append((result['lat2'], result['lon2']))
        
    if circle_points:
        circle_points.append(circle_points[0])
    
    lat = []
    lon = []
    for x in circle_points:
        lat.append(x[0])
        lon.append(x[1])

    return (lat, lon)

ninty_circ = create_circle_coords(89.99)
eighty_circ = create_circle_coords(80)
seventy_circ = create_circle_coords(70)
sixty_circ = create_circle_coords(60)
fifty_circ = create_circle_coords(50)
fourty_circ = create_circle_coords(40)
thirty_circ = create_circle_coords(30)
twenty_circ = create_circle_coords(20)
ten_circ = create_circle_coords(10)

fig = go.Figure((go.Scattergeo(
    lat = [center_lat],
    lon = [center_lon],
    marker = { 'size': 10, 'color': "orange" }),
    go.Scattergeo(
    fill = "toself",
    lat = ninty_circ[0],
    lon = ninty_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = eighty_circ[0],
    lon = eighty_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = seventy_circ[0],
    lon = seventy_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = sixty_circ[0],
    lon = sixty_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = fifty_circ[0],
    lon = fifty_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = fourty_circ[0],
    lon = fourty_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = thirty_circ[0],
    lon = thirty_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = twenty_circ[0],
    lon = twenty_circ[1],
    marker = {'size': 0.01}),
    go.Scattergeo(
    fill = "toself",
    lat = ten_circ[0],
    lon = ten_circ[1],
    marker = {'size': 0.01})))

fig.update_layout(
    map = {
        'style': "open-street-map",
        'center': {'lat': center_lat, 'lon': center_lon},
        'zoom': 1},
    showlegend = False)

#fig.update_geos(projection_type="orthographic")
fig.show()