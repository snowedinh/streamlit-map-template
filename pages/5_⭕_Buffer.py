import pandas as pd
import folium
from shapely.geometry import Point
import streamlit as st
from streamlit_folium import st_folium
# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震視覺化系统")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo)

# 加载地震震源数据
@st.cache_data
def load_data():
    url = "https://github.com/snowedinh/streamlit-map-template/raw/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%9C%81%E4%B8%89%E7%BA%A7%E4%BB%A5%E4%B8%8A%E5%9C%B0%E9%9C%87%E4%BF%A1%E6%81%AF_0.csv"
    data = pd.read_csv(url, encoding="gbk")
    return data

# 计算缓冲区
def create_buffer(lat, lon, radius_km):
    point = Point(lon, lat)
    buffer = point.buffer(radius_km)  # 半径单位为公里
    return buffer

# 可视化地震震源和缓冲区
def visualize_earthquake_with_buffer(data, buffer_radius_km):
    # 创建基础地图
    m = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=7)

    # 遍历数据并绘制地震震源和缓冲区
    for _, row in data.iterrows():
        lat, lon = row['Lat'], row['Lon']
        
        # 绘制地震震源位置红点
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
        ).add_to(m)
        
        # 绘制缓冲区
        buffer = create_buffer(lat, lon, buffer_radius_km)
        folium.GeoJson(buffer).add_to(m)
    
    return m

# 主程序
st.title("四川省地震緩衝區分析")

# 用户输入缓冲区半径
buffer_radius_km = st.number_input(
    "請輸入緩衝區的半徑（單位：度 ）（1度≈111公里）：",
    min_value=0.1,  # 设置最小值为0.1公里
    value=0.5,  # 默认值为0.5公里
    step=0.1,  # 每次步进0.1公里
)

# 加载地震数据
earthquake_data = load_data()

# 生成地图
st.write(f"### 以 {buffer_radius_km} 度為半徑進行緩衝區分析")
m = visualize_earthquake_with_buffer(earthquake_data, buffer_radius_km)

# 在Streamlit中显示地图
st_folium(m, width=725)
