import folium

# Center near the given coordinates (average for rough center)
center_lat = (35.4538 + 35.4762 + 35.4782 + 35.4558) / 4
center_lon = (-82.9828 + -82.9804 + -83.0078 + -83.0103) / 4

# Coordinates (lat, lon) for folium
coords = [
    [35.4538, -82.9828],
    [35.4762, -82.9804],
    [35.4782, -83.0078],
    [35.4558, -83.0103],
    [35.4538, -82.9828]
]

# Create map centered near Waynesville, NC
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Add polygon
folium.Polygon(
    locations=coords,
    color='blue',
    fill=True,
    fill_opacity=0.3,
    popup='Custom Square'
).add_to(m)

# Optional: Add marker for Waynesville
folium.Marker([35.4887, -82.9881], popup='Waynesville, NC').add_to(m)

m.save('waynesville_polygon_map.html')
