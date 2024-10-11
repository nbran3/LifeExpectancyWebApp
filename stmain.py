import json
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium

# Set page config
st.set_page_config(layout="wide", page_title="World Life Expectancy Map")

# Load and process data
@st.cache_data
def load_and_process_data():
    data = pd.read_csv(r"lifeExp.csv")
    data['Value'] = data['Value'].round().astype(int)
    median_value = data['Value'].median()
    data = data[['SpatialCode', 'Value']]
    return data, median_value

data, median_value = load_and_process_data()

# Load GeoJSON data
@st.cache_data
def load_geojson():
    with open(r"countries.geojson", 'r') as geojson_file:
        return json.load(geojson_file)

geojson_data = load_geojson()

# Update GeoJSON with life expectancy data
@st.cache_data
def update_geojson(geojson_data, data, median_value):
    countries_gdp_mapping = data.to_dict('records')
    for feature in geojson_data['features']:
        SpatialCode = feature['properties']['ISO_A3']
        found = False
        for mapping in countries_gdp_mapping:
            if mapping['SpatialCode'] == SpatialCode:
                feature['properties']['Value'] = mapping['Value']
                found = True
                break
        if not found:
            feature['properties']['Value'] = median_value
    return geojson_data

updated_geojson = update_geojson(geojson_data, data, median_value)

# Create Folium map
def create_map():
    m = folium.Map(location=[46.879002, -103.789879], zoom_start=5.4,
                   tiles=r'https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
                   attr="World Life Expectancy 2022 Choropleth map.")

    folium.Choropleth(
        geo_data=updated_geojson,
        name='World Life Exp 2022',
        data=data,
        columns=['SpatialCode', 'Value'],
        key_on='properties.ISO_A3',
        fill_color='Pastel1',
        fill_opacity=1,
        line_opacity=1,
        nan_fill_color='#f2efe9',
        line_color='white'
    ).add_to(m)

    g = folium.GeoJson(
        updated_geojson,
        name='geojson'
    ).add_to(m)

    folium.GeoJsonTooltip(fields=['ADMIN', 'Value'], aliases=["Country Name", "Life Expectancy"]).add_to(g)

    return m

# Streamlit app
st.title("World Life Expectancy Map")

# Create and display the map
map = create_map()
folium_static(map, width=1200, height=600)

# Optional: Display data table
if st.checkbox("Show Data Table"):
    st.write(data)

# Optional: Add more Streamlit widgets or displays as needed
st.sidebar.info("This map shows life expectancy data for countries around the world.")
st.sidebar.write(f"Median Life Expectancy: {median_value}")
