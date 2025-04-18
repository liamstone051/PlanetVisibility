from ZenithLocator import *
import numpy as np
import pandas as pd
from geopy.distance import great_circle


center_coords = zenith_locator(Jupiter)
center_lat = center_coords[0]
center_lon = center_coords[1]

earth_radius = 6371000  # in meters
distance_m = earth_radius * (np.pi / 2)
distance_m_div = distance_m / 9
bearings_deg = np.linspace(0, 360 - 360 / 720, 720)

for x in range(1, 2):
    circle_points = []
    for bearing in bearings_deg:
        destination = great_circle(distance_m_div * x).destination((center_lat, center_lon), bearing) # This does not work
        circle_points.append([destination.longitude, destination.latitude])
    circle_points_df = pd.DataFrame(circle_points, columns=['lon', 'lat'])
    print(circle_points_df)
