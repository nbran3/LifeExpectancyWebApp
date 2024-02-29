import folium
import os
import json
import pandas as pd
from app import get_data

data = None
def df_function():
    global data
    data = get_data()

if __name__ == '__main__':
    df_function()

df_function()

data = pd.DataFrame(data)
data['Value'] = data['Value'].round().astype(int)
median_value = data['Value'].median()

data= data[['SpatialCode', 'Value']]

dataJSON=data

countriesJSON = os.path.join('data', 'countries.geojson')

countries_gdp_mapping = dataJSON.to_json(orient='records')
countries_gdp_mapping = json.loads(countries_gdp_mapping)


"""with open(r'/Users/noahbrannon/Python/LifeExpApp/data/countries.geojson', 'r') as geojson_file:
    geojson_data = json.load(geojson_file)

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

with open('updated_geojson.json', 'w') as updated_geojson_file:
    json.dump(geojson_data, updated_geojson_file, indent=2)"""


map = folium.Map(location=[46.879002,-103.789879], zoom_start=5.4, tiles=r'https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', attr="US GDP 2022 Choropleth map by county.")

folium.Choropleth(
    geo_data = countriesJSON,
    name = 'World Life Exp 2022',
    data = data,
    columns = ['SpatialCode' , 'Value'],
    key_on = 'properties.ISO_A3',
    fill_color = 'Pastel1',
    fill_opacity = 1,
    line_opacity = 1,
    nan_fill_color = '#f2efe9',
    line_color = 'white'
).add_to(map)

SQLJson = os.path.join('data', 'updated_geojson.json')

### This is to add a hover effect when the cursor is above a county, it will display its name. I tried to add the GDP result but since that is in a SQL query its a bit hard to add to a JSON file. 
g = folium.GeoJson(
    SQLJson,
    name='geojson'
).add_to(map)

folium.GeoJsonTooltip(fields=['ADMIN', 'Value'], aliases=["Country Name", "Life Expectancy"]).add_to(g)

### Save to index.html and then view it in the browser  
map.save('index.html')
