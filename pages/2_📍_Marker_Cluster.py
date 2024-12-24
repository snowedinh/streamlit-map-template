import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import pairwise_distances

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo)

st.title("标记震源与监测站位置的回归分析地图")

with st.expander("See source code"):
    with st.echo():
        # 创建地图
        m = leafmap.Map(center=[40, -100], zoom=4)

        # 文件路径
        cities_url = "https://github.com/snowedinh/streamlit-map-template/raw/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%9C%81%E4%B8%89%E7%BA%A7%E4%BB%A5%E4%B8%8A%E5%9C%B0%E9%9C%87%E4%BF%A1%E6%81%AF_0.csv"
        regions_url = "https://geojson.cn/api/china/510000.json"
        stations_url = "https://github.com/snowedinh/streamlit-map-template/raw/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%9C%81%E5%9C%B0%E9%9C%87%E7%9B%91%E6%B5%8B%E7%AB%99%E7%82%B9%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF_0.csv"

        # 加载城市数据
        try:
            cities = pd.read_csv(cities_url, encoding="gbk")  
            st.write("Cities data loaded successfully:")
            st.write(cities.head()) 
        except UnicodeDecodeError as e:
            st.error(f"Error loading cities data: {e}")
            cities = pd.DataFrame()  

        # 加载 GeoJSON 文件
        try:
            m.add_geojson(regions_url, layer_name="Sichuan Region")
        except Exception as e:
            st.error(f"Error loading GeoJSON data: {e}")

        # 加载监测站数据
        try:
            stations = pd.read_csv(stations_url, encoding="gbk")
            st.write("Seismic stations data loaded successfully:")
            st.write(stations.head())
        except UnicodeDecodeError as e:
            st.error(f"Error loading seismic stations data: {e}")
            stations = pd.DataFrame()

        # 添加城市点数据到地图
        if not cities.empty and "Lon" in cities.columns and "Lat" in cities.columns:
            m.add_points_from_xy(
                cities,
                x="Lon",
                y="Lat",
                color_column=None,  
                icon_names=["gear", "map", "leaf", "globe"],
                spin=True,
                add_legend=True,
            )
        else:
            st.error("Cities data is empty or missing required columns ('Lon', 'Lat').")

        # 添加监测站点数据到地图
        if not stations.empty and "Lon" in stations.columns and "Lat" in stations.columns:
            m.add_points_from_xy(
                stations,
                x="Lon",
                y="Lat",
                color_column=None,
                icon_names=["cloud", "cloud-rain", "wind"],
                spin=True,
                add_legend=True,
            )
        else:
            st.error("Seismic stations data is empty or missing required columns ('Lon', 'Lat').")

        # 展示地图
        m.to_streamlit(height=700)

        # 回归分析：监测站与震源点位置的相关性
        if not stations.empty and not cities.empty:
            # 监测站点的经纬度
            station_coords = stations[["Lon", "Lat"]]

            # 平均震源点位置
            city_coords = cities[["Lon", "Lat"]].mean(axis=0)

            # 计算监测站点到震源点的距离
            distances = pairwise_distances(station_coords, [city_coords], metric='euclidean')

            # 使用距离作为目标变量
            y = distances.flatten()  # 转换为一维数组
            X = station_coords  # 特征变量（经纬度）

            # 线性回归
            model = LinearRegression()
            model.fit(X, y)

            # 预测值
            predictions = model.predict(X)

            # 绘制回归图
            plt.figure(figsize=(10, 6))
            sns.regplot(x=stations["Lon"], y=stations["Lat"],
                        scatter_kws={'s': 50, 'color': 'blue'}, line_kws={'color': 'red'})
            plt.title("Regression between Seismic Station Locations and Earthquake Source Locations")
            plt.xlabel("Longitude of Seismic Station")
            plt.ylabel("Latitude of Seismic Station")
            st.pyplot(plt)
        else:
            st.error("Seismic stations or cities data are missing for regression analysis.")
