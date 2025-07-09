from ZenithLocator import *
import numpy as np
from geopy.distance import Geodesic
import plotly.graph_objects as go
import dash
from dash import dcc, html, Output, Input
import plotly.io as pio
pio.renderers.default = "browser"

planet_names = [
    "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune",
    "Pluto", "Moon"
]

planet_centers = {}

# Getting zenith of each planets from ZenithLocator.py
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

# Function to create visibility rings based on visibility range
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

# Creating visibility rings
for planet, (lat, lon) in planet_centers.items():
    planet_rings[planet] = {}
    for deg in ring_degrees:
        key = f"{int(deg)}°" if deg != 89.99 else "90°"
        planet_rings[planet][key] = create_circle_coords(deg, lat, lon)

mercury_cols = ["#e8e0d8", "#d8cfc3", "#c8beb0", "#b8ae9d", "#a8988a", "#948374", "#7f6d5f", "#69594c", "#53443a"]
venus_cols   = ["#fff8ef", "#fde8d6", "#facfb9", "#f9b999", "#f5a574", "#e98d5a", "#d57646", "#b85c37", "#9f4a2e"]
mars_cols    = ["#f7dad4", "#f1a69d", "#e76b61", "#d84d44", "#bf382f", "#a32f27", "#85261d", "#671b14", "#4b130d"]
jupiter_cols = ["#f4b08a", "#e49063", "#d8743d", "#c55a27", "#aa451f", "#8e371a", "#712c15", "#55200f", "#3a140a"]
saturn_cols  = ["#fbeec1", "#fae4a1", "#f6d874", "#ebb847", "#d9992e", "#d28d26", "#c97e1f", "#bc7018", "#ae6010"]
uranus_cols  = ["#e9fcf9", "#c5f2ed", "#a2e8e3", "#7eddd7", "#5bd2cb", "#45bec2", "#32aab2", "#258e97", "#1a737c"]
neptune_cols = ["#e2f0ff", "#badcff", "#91c7ff", "#67b2ff", "#499cf0", "#3b87d9", "#2d72c2", "#1f5daa", "#16498f"]
pluto_cols   = ["#f0f4fb", "#d7dfee", "#c1cade", "#abb5ce", "#969fbe", "#828aaf", "#6e769f", "#5a628f", "#464f7f"]
moon_cols    = ["#f4f4f4", "#dfe0e2", "#c8cad0", "#b2b4ba", "#9c9ea6", "#858890", "#6f727a", "#5a5c63", "#46474d"]

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
    html.Div([
        html.H2("Planetary Zenith Rings", style={
            "margin": "0 0 8px 0",
            "fontFamily": "Segoe UI",
            "fontSize": "22px",
            "color": "#2c3e50"
        }),
        html.P("Each ring shows where the planet appears at a specific altitude above the horizon. "
            "The outermost ring starts at 0° (planet is along the horizon) and each contour represents an additional 10°, up to the center which marks the zenith at 90° (directly overhead).",
            style={
                "margin": "0 0 15px 0",
                "fontFamily": "Segoe UI",
                "fontSize": "14px",
                "color": "#555"
        }),
        html.H4("Select Planet Rings", style={
            "margin": "0 0 10px 0",
            "fontFamily": "Segoe UI",
            "color": "#2c3e50"
        }),
        dcc.Checklist(
            id='ring-group-toggle',
            options=[{'label': group, 'value': group} for group in grouped_circles],
            value=["Moon"],
            labelStyle={
                "display": "block",
                "marginBottom": "6px",
                "fontFamily": "Segoe UI",
                "fontSize": "15px",
                "color": "#34495e"
            }
        )
    ], style={
        "position": "absolute",
        "top": "20px",
        "left": "20px",
        "zIndex": 999,
        "maxHeight": "90vh",
        "overflowY": "auto",
        "width": "260px",
        "background": "white",
        "padding": "20px 12px 20px 20px",
        "borderRadius": "10px",
        "boxShadow": "0 4px 16px rgba(0, 0, 0, 0.15)"
    }),
    dcc.Graph(
        id='map',
        style={"height": "100vh", "width": "100vw"},
        config={"scrollZoom": True}
    )
], style={
    "margin": 0,
    "padding": 0,
    "overflow": "hidden",
    "fontFamily": "Segoe UI, Arial, sans-serif"
})

@app.callback(
    Output('map', 'figure'),
    Input('ring-group-toggle', 'value')
)
def update_map(selected_groups):
    fig = go.Figure()

    # If nothing is selected, show an invisible point to keep the map on screen
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

            # Adding the center marker for each planet
            fig.add_trace(go.Scattergeo(
                lat=[center_lat],
                lon=[center_lon],
                mode='markers',
                marker=dict(size=10, 
                            color='black',
                            reversescale = True
                            ),
                name=f"{planet} Zenith"
            ))

            labels = [label for label, _, _ in data['rings']]

            # Adding each visibility rings for the planets
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
        uirevision="map-position",
        showlegend=False,
        geo=dict(
            scope='world',
            showland=True,
            projection=dict(type='equirectangular'),
            lataxis=dict(range=[-85, 85]),
            lonaxis=dict(range=[-180, 180]),
            fitbounds="locations"
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

# Running the program
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
