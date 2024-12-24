import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo)


st.title("標記叢集地圖")

with st.expander("See source code"):
    with st.echo():
        # 创建地图
        m = leafmap.Map(center=[40, -100], zoom=4)

        # 文件路径
        cities_url = "https://github.com/snowedinh/streamlit-map-template/raw/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%9C%81%E4%B8%89%E7%BA%A7%E4%BB%A5%E4%B8%8A%E5%9C%B0%E9%9C%87%E4%BF%A1%E6%81%AF_0.csv"
        regions_url = "https://geojson.cn/api/china/510000.json"

        # 加载CSV文件
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

        # 添加点数据到地图
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

m.to_streamlit(height=700)
