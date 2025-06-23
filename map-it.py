import folium

# Coordinates (lat, lon) for folium
coords = [
    [35.4661, -82.5387],
    [35.488499999999995, -82.5361],
    [35.49059999999999, -82.5635999],
    [35.468199999999996, -82.5661],
    [35.4661, -82.5387],
]

# Calculate center from new coords
lats = [lat for lat, lon in coords]
lons = [lon for lat, lon in coords]
center_lat = sum(lats) / len(lats)
center_lon = sum(lons) / len(lons)

# Create map centered near Waynesville, NC
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Add polygon
folium.Polygon(
    locations=coords, color="blue", fill=True, fill_opacity=0.3, popup="Custom Square"
).add_to(m)

# Optional: Add marker for Waynesville
folium.Marker([35.4887, -82.9881], popup="Waynesville, NC").add_to(m)

m.save("weather_map.html")
