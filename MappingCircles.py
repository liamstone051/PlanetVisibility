from ZenithLocator import *
import numpy as np
import pandas as pd
from geopy.distance import Geodesic
import plotly.graph_objects as go

import dash
from dash import dcc, html, Output, Input
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = "browser"

planet_names = [
    "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune",
    "Pluto", "Moon"
]

planet_centers = {}

print(zenith_locator(Jupiter))

for name in planet_names:
    coords = zenith_locator(globals()[name])
    planet_centers[name] = {
        "lat": coords[0],
        "lon": coords[1]
    }

earth_radius = 6371000  # in meters
distance_m = earth_radius * (np.pi / 2)
distance_m_div = distance_m / 9
bearings_deg = np.linspace(0, 360 - 360 / 720, 720)

def create_circle_coords(radius_deg, center_lat, center_lon, num_points=32):
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

ring_degrees = [89.99, 80, 70, 60, 50, 40, 30, 20, 10]

planet_centers = {
    "Mercury": (planet_centers["Mercury"]["lat"], planet_centers["Mercury"]["lon"]),
    "Venus": (planet_centers["Venus"]["lat"], planet_centers["Venus"]["lon"]),
    "Mars": (planet_centers["Mars"]["lat"], planet_centers["Mars"]["lon"]),
    "Jupiter": (planet_centers["Jupiter"]["lat"], planet_centers["Jupiter"]["lon"]),
    "Saturn": (planet_centers["Saturn"]["lat"], planet_centers["Saturn"]["lon"]),
    "Uranus": (planet_centers["Uranus"]["lat"], planet_centers["Uranus"]["lon"]),
    "Neptune": (planet_centers["Neptune"]["lat"], planet_centers["Neptune"]["lon"]),
    "Pluto": (planet_centers["Pluto"]["lat"], planet_centers["Pluto"]["lon"]),
    "Moon": (planet_centers["Moon"]["lat"], planet_centers["Moon"]["lon"])
}

planet_rings = {}

for planet, (lat, lon) in planet_centers.items():
    planet_rings[planet] = {}
    for deg in ring_degrees:
        key = f"{int(deg)}°" if deg != 89.99 else "90°"
        planet_rings[planet][key] = create_circle_coords(deg, lat, lon)

mercury_cols = [
    "#e8e0d8",  # soft warm grey
    "#d8cfc3",  # sandy grey
    "#c8beb0",  # ash grey
    "#b8ae9d",  # warm taupe
    "#a8988a",  # warm mineral
    "#948374",  # smoky bronze
    "#7f6d5f",  # deep taupe
    "#69594c",  # volcanic dust
    "#53443a"   # metal-stone
]
venus_cols = [
    "#fff8ef",  # creamy ivory
    "#fde8d6",  # soft warm cream
    "#facfb9",  # light peach
    "#f9b999",  # warm apricot
    "#f5a574",  # richer peach
    "#e98d5a",  # warm coral
    "#d57646",  # burnt apricot
    "#b85c37",  # warm sienna
    "#9f4a2e"   # deep terracotta
]
mars_cols = [
    "#f7dad4",  # soft rose pink
    "#f1a69d",  # warm coral red
    "#e76b61",  # tomato red
    "#d84d44",  # rusty red
    "#bf382f",  # deep brick red
    "#a32f27",  # burnt crimson
    "#85261d",  # dark rust red
    "#671b14",  # deep maroon
    "#4b130d"   # almost black red
]
jupiter_cols = [
    "#f4b08a",  # light warm tan
    "#e49063",  # soft pumpkin
    "#d8743d",  # burnt orange
    "#c55a27",  # deep rust
    "#aa451f",  # rich sienna
    "#8e371a",  # dark burnt umber
    "#712c15",  # deep rust brown
    "#55200f",  # dark terra cotta
    "#3a140a"   # almost black rust
]

saturn_cols = [
    "#fbeec1",  # soft buttery cream
    "#fae4a1",  # lighter warm pale yellow (lightened)
    "#f6d874",  # lighter golden yellow (lightened)
    "#ebb847",  # lighter rich amber (lightened)
    "#d9992e",  # warm goldenrod (unchanged)
    "#d28d26",  # slightly darker bright golden amber
    "#c97e1f",  # slightly darker glowing amber
    "#bc7018",  # slightly darker vibrant gold
    "#ae6010"   # darker sunny golden yellow (darkened)
]
uranus_cols = [
    "#e9fcf9",  # icy white
    "#c5f2ed",  # pale mint
    "#a2e8e3",  # soft aqua
    "#7eddd7",  # seafoam
    "#5bd2cb",  # turquoise
    "#45bec2",  # soft teal
    "#32aab2",  # medium teal
    "#258e97",  # darker teal
    "#1a737c"   # deep icy green
]
neptune_cols = [
    "#e2f0ff",  # light icy blue
    "#badcff",  # sky blue
    "#91c7ff",  # soft azure
    "#67b2ff",  # true blue
    "#499cf0",  # vivid blue
    "#3b87d9",  # deeper ocean blue
    "#2d72c2",  # cobalt
    "#1f5daa",  # indigo blue
    "#16498f"   # deep sea blue
]
pluto_cols = [
    "#f0f4fb",  # frosty white
    "#d7dfee",  # icy blue-grey
    "#c1cade",  # cold haze
    "#abb5ce",  # muted icy lavender
    "#969fbe",  # twilight frost
    "#828aaf",  # cold dusk
    "#6e769f",  # icy steel
    "#5a628f",  # deep frost
    "#464f7f"   # distant cold
]
moon_cols = [
    "#f4f4f4",  # pale moonlight
    "#dfe0e2",  # moon dust
    "#c8cad0",  # crater grey
    "#b2b4ba",  # shadow grey
    "#9c9ea6",  # neutral grey
    "#858890",  # moonstone
    "#6f727a",  # shaded crater
    "#5a5c63",  # dark regolith
    "#46474d"   # deep shadow
]

grouped_circles = {
    name: {
        "center": planet_centers[name],
        "rings": [
            (label, planet_rings[name][label], globals()[f"{name.lower()}_cols"][i])
            for i, label in enumerate(planet_rings[name])
        ]
    }
    for name in planet_centers
}


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Checklist(
        id='ring-group-toggle',
        options=[{'label': group, 'value': group} for group in grouped_circles],
        value=["Moon"],
        labelStyle={'display': 'block'},
        style={
            "position": "absolute", "top": "10px", "left": "10px",
            "zIndex": 999, "background": "white", "padding": "10px"
        }
    ),
    dcc.Graph(
        id='map',
        style={"height": "100vh", "width": "100vw"},
        config={"scrollZoom": True}
    )
], style={"margin": 0, "padding": 0, "overflow": "hidden"})

@app.callback(
    Output('map', 'figure'),
    Input('ring-group-toggle', 'value')
)
def update_map(selected_groups):
    fig = go.Figure()

    # If nothing is selected, show a dummy invisible marker to preserve the map
    if not selected_groups:
        fig.add_trace(go.Scattergeo(
            lat=[0],
            lon=[0],
            mode='markers',
            marker=dict(size=0.1, color='rgba(0,0,0,0)'),
            showlegend=False,
            hoverinfo='skip',
            name='dummy'
        ))

    for planet, data in grouped_circles.items():
        if planet in selected_groups:
            center_lat, center_lon = data['center']

            fig.add_trace(go.Scattergeo(
                lat=[center_lat],
                lon=[center_lon],
                mode='markers',
                marker=dict(size=10, color='black'),
                name=f"{planet} Zenith"
            ))

            labels = [label for label, _, _ in data['rings']]

            for i, label in enumerate(reversed(labels)):
                numeric_value = int(label.strip("°")) - 10
                new_label = f"{numeric_value}°"

                coords = data['rings'][i][1]
                color = data['rings'][i][2]

                fig.add_trace(go.Scattergeo(
                    fill="toself",
                    mode="lines",
                    lat=coords[0],
                    lon=coords[1],
                    line=dict(color=color),
                    name=f"{planet} - {new_label}",
                    opacity=0.3,
                    hoverinfo='skip'
                ))

    fig.update_layout(
        uirevision="map-position",  # preserve zoom/pan
        showlegend=False,
        geo=dict(
            scope='world',
            showland=True,
            projection=dict(type='equirectangular'),
            lataxis=dict(range=[-85, 85]),
            lonaxis=dict(range=[-180, 180]),
            fitbounds="locations"                      # auto-fit data when possible
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
