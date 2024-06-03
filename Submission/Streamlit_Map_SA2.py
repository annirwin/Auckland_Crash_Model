import streamlit as st
import folium
from streamlit_folium import folium_static
from pyproj import Transformer

# Colour maps
import matplotlib as mpl
import matplotlib.colors as mcolors

# Data manipulation
import pandas as pd
import re

# DATA PROCESSING

# STEP 1 : Convert all the mesh block data points to WGS84 (latitude/longitude) for plotting on map
# Read in file
file_path = 'output_crash.csv'
columns_to_import = ['WKT', 'SA2_Name', 'SA22023_V1']
mesh_blocks = pd.read_csv(file_path, usecols=columns_to_import)
print(mesh_blocks)

# Convert "WKT" to list with a polygon string for each row
coordinates = mesh_blocks['WKT'].astype(str).tolist()

# Converts str list format to standard lon, lat coordinates.
# New Zealand Transverse Mercator 2000 to EPSG:4326 WGS 84
def convert_epsg_to_stdlonlat(coordinates_list):
    polygon_coords_list = []

    def convert_long_lat_pairs(coords):
        # Find all numeric values in the string
        numeric_values = re.findall(r'-?\d+\.\d+', coords)

        # Ensure that we have an even number of numeric values
        if len(numeric_values) % 2 != 0:
            return []

        # Convert numeric values to pairs of longitude and latitude enclosed in square brackets
        pairs = [[float(numeric_values[i]), float(numeric_values[i+1])] for i in range(0, len(numeric_values), 2)]
        
        return pairs

    # Define the EPSG codes
    input_epsg = 'EPSG:2193'  # New Zealand Transverse Mercator 2000
    output_epsg = 'EPSG:4326'  # WGS84 (latitude/longitude)

    # Create a PyProj transformer
    transformer = Transformer.from_crs(input_epsg, output_epsg)

    for coords in coordinates_list:
        # Convert coordinates to long/lat pairs
        coordinate_pairs = convert_long_lat_pairs(coords)
        
        # Skip invalid coordinate pairs
        if not coordinate_pairs:
            continue
        
        # Initialize an empty list to store coordinate pairs
        polygon_coords = []
        
        # Loop through each coordinate pair
        for pair in coordinate_pairs:
            # Convert coordinates from EPSG:2193 to EPSG:4326
            lon, lat = transformer.transform(pair[1], pair[0])
            polygon_coords.append([lon, lat])  # Append the coordinate pair to the list
        
        # Append the list of coordinate pairs for this polygon to the main list
        polygon_coords_list.append(polygon_coords)

    return polygon_coords_list

polygon_coords_list = convert_epsg_to_stdlonlat(coordinates)

# STEP 2: Create Tooltip files from SA2_Name
tooltips = mesh_blocks['SA2_Name'].astype(str).tolist()

# STEP 3: Colour code SA2 Areas

# Generate a list of unique SA2 values
SA2 = mesh_blocks['SA22023_V1'].astype(str).tolist()
distinct_SA2 = list(set(SA2))

# Get the tab20 colormap
colormap = mpl.colormaps.get_cmap('tab20')

# Map each SA2 to a color in the colormap and convert to hex
colors = {sa2: mcolors.to_hex(colormap(i % colormap.N)) for i, sa2 in enumerate(distinct_SA2)}

# Convert SA22023_V1 values to strings before mapping so that data types match
mesh_blocks['SA22023_V1_str'] = mesh_blocks['SA22023_V1'].astype(str)

# Add a new column to the DataFrame with the colors
mesh_blocks['Color'] = mesh_blocks['SA22023_V1_str'].map(colors)

# Drop temp column
mesh_blocks.drop(columns=['SA22023_V1_str'], inplace=True)

# Create a list from the DataFrame
color_list = mesh_blocks['Color'].values.tolist()

# CREATE MAP IN STREAMLIT

# Set up the Streamlit app
st.title("Auckland City Crash Model")

# Create a folium map centered around Auckland, New Zealand
m = folium.Map(location=[-36.8485, 174.7633], zoom_start=12)

# Add mesh block tile layer to the map
folium.TileLayer('openstreetmap').add_to(m)

# Add polygons representing mesh blocks to the map
for i in range(len(polygon_coords_list)):
    poly = polygon_coords_list[i]
    folium.Polygon(locations=poly, color=color_list[i], weight=1.5, fill=True, fill_color=color_list[i], 
                   fill_opacity=0.1, tooltip=tooltips[i]).add_to(m)

# Display the map with the polygon in the Streamlit app
folium_static(m, width=1000)
