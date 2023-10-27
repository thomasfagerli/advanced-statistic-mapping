import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.worlddata.info/average-penissize.php'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# Finding the table
table = soup.find('table')

# Extracting headers
headers = [header.text for header in table.find_all('th')]

# Extracting rows
rows = table.find_all('tr')
data = []
for row in rows[1:]:
    cells = row.find_all('td')
    data.append([cell.text for cell in cells])

# Creating a dataframe
df = pd.DataFrame(data, columns=headers)
df['Erect length'] = df['Erect length'].str.replace(' cm', '').astype(float)

import folium
import geopandas as gpd

# Load the world map dataset available in geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge your data with the world map data on the 'country' column
merged = world.set_index('name').join(df.set_index('Country'))

# Create a map object
m = folium.Map(location=[20,0], zoom_start=2)

# Plot the data on the map
folium.Choropleth(
    geo_data=merged,
    name='choropleth',
    data=df,
    columns=['Country', 'Erect length'],
    key_on='feature.id',
    fill_color='RdYlGn',   # This color scale will go from green for low values to red for high values
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Value'
).add_to(m)