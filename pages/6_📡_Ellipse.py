import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import numpy as np
from scipy.stats import chi2
import folium
from math import pi, cos, sin
import altair as alt
from streamlit_folium import st_folium

# Set page config
st.set_page_config(layout="wide")

# Sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo)


st.title("標准差橢圓")

# Load data with explicit encoding
@st.cache_data
def load_data():
    earthquake_url = "https://github.com/snowedinh/streamlit-map-template/raw/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%9C%81%E4%B8%89%E7%BA%A7%E4%BB%A5%E4%B8%8A%E5%9C%B0%E9%9C%87%E4%BF%A1%E6%81%AF_0.csv"
    station_url = "https://github.com/snowedinh/streamlit-map-template/raw/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%9C%81%E5%9C%B0%E9%9C%87%E7%9B%91%E6%B5%8B%E7%AB%99%E7%82%B9%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF_0.csv"
    
    try:
        earthquakes_df = pd.read_csv(earthquake_url, encoding='gb18030')
        stations_df = pd.read_csv(station_url, encoding='gb18030')
    except:
        try:
            earthquakes_df = pd.read_csv(earthquake_url, encoding='gbk')
            stations_df = pd.read_csv(station_url, encoding='gbk')
        except:
            earthquakes_df = pd.read_csv(earthquake_url, encoding='gb2312')
            stations_df = pd.read_csv(station_url, encoding='gb2312')
    
    return earthquakes_df, stations_df

earthquakes_df, stations_df = load_data()

# Calculate Standard Deviation Ellipse
def calculate_sde(df, lon_col, lat_col):
    x = df[lon_col].values
    y = df[lat_col].values
    
    # Calculate mean center
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Calculate deviation scores
    dx = x - mean_x
    dy = y - mean_y
    
    # Calculate variance and covariance
    var_x = np.mean(dx**2)
    var_y = np.mean(dy**2)
    cov_xy = np.mean(dx * dy)
    
    # Calculate rotation angle
    theta = 0.5 * np.arctan2(2 * cov_xy, var_x - var_y)
    
    # Calculate semi-major and semi-minor axes
    a = np.sqrt(2 * chi2.ppf(0.95, 2) * 
                ((var_x + var_y) / 2 + np.sqrt(((var_x - var_y) / 2)**2 + cov_xy**2)))
    b = np.sqrt(2 * chi2.ppf(0.95, 2) * 
                ((var_x + var_y) / 2 - np.sqrt(((var_x - var_y) / 2)**2 + cov_xy**2)))
    
    # Calculate area and flattening ratio
    area = pi * a * b
    flattening = (a - b) / a
    
    return mean_x, mean_y, theta, a, b, area, flattening

# Calculate ellipse points
def get_ellipse_points(center_x, center_y, a, b, theta, num_points=68):
    points = []
    for i in range(num_points):
        angle = (2 * pi * i) / num_points
        x = a * cos(angle)
        y = b * sin(angle)
        
        # Rotate and translate
        rotated_x = x * cos(theta) - y * sin(theta) + center_x
        rotated_y = x * sin(theta) + y * cos(theta) + center_y
        
        points.append([rotated_y, rotated_x])  # Note: Leaflet uses [lat, lon]
    return points

# Create map
m = folium.Map(location=[30.5, 104], zoom_start=7, tiles='OpenStreetMap')

# Create feature groups for different layers
earthquakes = folium.FeatureGroup(name="地震事件 (粉色)")
stations = folium.FeatureGroup(name="监测站点 (浅蓝)")

# Add earthquake points with light pink color
for idx, row in earthquakes_df.iterrows():
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=5,
        color='#FFB6C1',  # Light pink
        fill=True,
        fillOpacity=0.7,
        popup=f"震级: {row['Data']}",
    ).add_to(earthquakes)

# Add station points with light blue color
for idx, row in stations_df.iterrows():
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=5,
        color='#ADD8E6',  # Light blue
        fill=True,
        fillOpacity=0.7,
        popup=f"站点: {row['name']}",
    ).add_to(stations)

# Calculate ellipses
eq_stats = calculate_sde(earthquakes_df, 'Lon', 'Lat')
st_stats = calculate_sde(stations_df, 'Lon', 'Lat')

# Add earthquake ellipse
eq_points = get_ellipse_points(eq_stats[0], eq_stats[1], eq_stats[3], eq_stats[4], eq_stats[2])
folium.PolyLine(
    eq_points,
    color='red',
    weight=2,
    opacity=0.8,
    popup='地震标准差椭圆'
).add_to(earthquakes)

# Add station ellipse
st_points = get_ellipse_points(st_stats[0], st_stats[1], st_stats[3], st_stats[4], st_stats[2])
folium.PolyLine(
    st_points,
    color='blue',
    weight=2,
    opacity=0.8,
    popup='站点标准差椭圆'
).add_to(stations)

# Add the feature groups to the map
earthquakes.add_to(m)
stations.add_to(m)


# Add layer control
folium.LayerControl().add_to(m)

# Convert to streamlit component
st_data = st_folium(m, width=800, height=600)

# Create comparison charts using Altair
st.subheader("關鍵性指標對比")

# Create two columns for separate charts
col1, col2 = st.columns(2)

# Prepare data for Area bar chart
area_data = pd.DataFrame({
    'Category': ['地震事件', '監測站點'],
    'Area': [eq_stats[5], st_stats[5]]
})

# Prepare data for Flattening Ratio bar chart
ratio_data = pd.DataFrame({
    'Category': ['地震事件', '監測站點'],
    'Ratio': [eq_stats[6], st_stats[6]]
})

with col1:
    area_chart = alt.Chart(area_data).mark_bar().encode(
        x=alt.X('Category:N', title='類別'),
        y=alt.Y('Area:Q', title='面積'),
        color=alt.Color('Category:N', 
                       scale=alt.Scale(domain=['地震事件', '監測站點'],
                                     range=['#FFB6C1', '#ADD8E6'])),
        tooltip=['Category', 'Area']
    ).properties(
        width=300,
        height=300,
        title='標準差橢圓面積分佈'
    ).configure_title(
        fontSize=16,
        anchor='middle'
    )
    st.altair_chart(area_chart, use_container_width=True)
    
    
with col2:
    
    ratio_chart = alt.Chart(ratio_data).mark_bar().encode(
        x=alt.X('Category:N', title='類別'),
        y=alt.Y('Ratio:Q', title='扁率'),
        color=alt.Color('Category:N', 
                       scale=alt.Scale(domain=['地震事件', '監測站點'],
                                     range=['#FFB6C1', '#ADD8E6'])),
        tooltip=['Category', 'Ratio']
    ).properties(
        width=300,
        height=300,
        title='扁率分布'
    ).configure_title(
        fontSize=16,
        anchor='middle'
    )
    st.altair_chart(ratio_chart, use_container_width=True)
    
   
