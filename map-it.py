"""Create a simple interactive map highlighting an area in Waynesville, NC.

This script demonstrates using [Folium](https://python-visualization.github.io/folium/)
to draw a polygon and save it to ``weather_map.html``. The map is centered on the
average of the provided coordinates and can be opened in any web browser.
"""

import folium

# Coordinates (latitude, longitude) used to draw the polygon
coords = [
    [35.4661, -82.5387],
    [35.488499999999995, -82.5361],
    [35.49059999999999, -82.5635999],
    [35.468199999999996, -82.5661],
    [35.4661, -82.5387],
]

# Determine map center by averaging the polygon coordinates
lats = [lat for lat, lon in coords]
lons = [lon for lat, lon in coords]
center_lat = sum(lats) / len(lats)
center_lon = sum(lons) / len(lons)

# Create the map centered near Waynesville, NC
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Add the polygon overlay
folium.Polygon(
    locations=coords, color="blue", fill=True, fill_opacity=0.3, popup="Custom Square"
).add_to(m)

# Optional: add a marker for Waynesville
folium.Marker([35.4887, -82.9881], popup="Waynesville, NC").add_to(m)

m.save("weather_map.html")
