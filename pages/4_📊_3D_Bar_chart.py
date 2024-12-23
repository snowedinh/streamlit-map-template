# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import altair as alt
from streamlit_echarts import st_echarts  # Import for ECharts integration

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="\u56db\u5ccc\u7701\u5730\u9707\u5206\u5e03\u53ef\u89c6\u5316", page_icon=":earth_asia:")
# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)
logo = "https://github.com/snowedinh/streamlit-map-template/edit/main/%E5%9C%B0%E9%9C%87.png"
st.sidebar.image(logo)

# LOAD DATA ONCE
@st.cache_data
def load_data():
    path = "https://github.com/snowedinh/streamlit-map-template/raw/refs/heads/main/%E5%9B%9B%E5%B7%9D%E7%9C%81%E4%B8%89%E7%BA%A7%E4%BB%A5%E4%B8%8A%E5%9C%B0%E9%9C%87%E4%BF%A1%E6%81%AF_0.csv"
    data = pd.read_csv(path, encoding="gbk")
    data["Month"] = pd.to_datetime(data["Time"].str.split('T').str[0], format="%m/%d").dt.month
    return data

# FUNCTION FOR MAP VISUALIZATION
def map(data, lat, lon, zoom, bearing):
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
                "bearing": bearing,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position="[Lon, Lat]",
                    radius=10000,
                    elevation_scale=50,
                    elevation_range=[0, 3000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )

# FILTER DATA FOR A SPECIFIC MONTH
@st.cache_data
def filter_data_by_month(df, month):
    return df[df["Month"] == month]

# CALCULATE MIDPOINT FOR MAP VIEW
@st.cache_data
def calculate_midpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# STREAMLIT APP LAYOUT
data = load_data()

# LAYING OUT THE TOP SECTION OF THE APP
st.title("四川省地震分布視覺化")
month_selected = st.slider(
    "滑動可選擇地震發生的月份", 1, 12, 1, key="selected_month"
)

# FILTER DATA BASED ON SELECTED MONTH
filtered_data = filter_data_by_month(data, month_selected)

# CALCULATE MIDPOINT
midpoint = calculate_midpoint(filtered_data["Lat"], filtered_data["Lon"])

# MAP ROTATION STATES
city_coords = {
    "宜賓市": (28.77, 104.62),
    "自貢市": (29.35, 104.77),
    "綿陽市": (31.46, 104.73),
}
if "global_bearing" not in st.session_state:
    st.session_state.global_bearing = 0
if "city_bearings" not in st.session_state:
    st.session_state.city_bearings = {city: 0 for city in ["全省"] + list(city_coords.keys())}

# DISPLAY MAIN MAP
st.write(f"### 四川省地震分布圖: {month_selected} 月")
map(filtered_data, midpoint[0], midpoint[1], 7, st.session_state.city_bearings["全省"])

col1, col2 = st.columns(2)
with col1:
    if st.button("順時針旋轉30度", key="global_cw"):
        st.session_state.city_bearings["全省"] += 30
        st.session_state.city_bearings["全省"] %= 360
with col2:
    if st.button("逆時針旋轉30度", key="global_ccw"):
        st.session_state.city_bearings["全省"] -= 30
        st.session_state.city_bearings["全省"] %= 360

# ADDITIONAL MAPS FOR SPECIFIC CITIES
for city, coords in city_coords.items():
    st.write(f"### {city} 地震分布視覺化 ({month_selected} 月)")
    city_data = filter_data_by_month(data, month_selected)
    map(city_data, coords[0], coords[1], 7, st.session_state.city_bearings[city])

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"順時針旋轉30度", key=f"{city}_cw"):
            st.session_state.city_bearings[city] += 30
            st.session_state.city_bearings[city] %= 360
    with col2:
        if st.button(f"逆時針旋轉30度", key=f"{city}_ccw"):
            st.session_state.city_bearings[city] -= 30
            st.session_state.city_bearings[city] %= 360

monthly_counts = data['Month'].value_counts().sort_index()
chart_data = pd.DataFrame({
    'Month': monthly_counts.index,
    'Counts': monthly_counts.values
})

# Select chart type (Altair or ECharts)
chart_type = st.radio("選擇統計圖表類型", ["Altair", "ECharts"])

if chart_type == "Altair":
    # 使用 Altair 绘制图表
    monthly_chart = (
        alt.Chart(chart_data)
        .mark_area(interpolate='step-after', opacity=0.2, color='red')
        .encode(
            x=alt.X('Month:O', title='月份', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Counts:Q', title='地震次數'),
            tooltip=['Month', 'Counts']
        )
        .properties(title='四川省月度地震分布圖', width='container', height=300)
    )

    # 在 Streamlit 中展示 Altair 图表
    st.altair_chart(monthly_chart, use_container_width=True)

elif chart_type == "ECharts":
    # 使用 ECharts 绘制图表
    echart_option = {
        "title": {"text": "四川省月度地震分布圖"},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"}
        },
        "xAxis": {
            "type": "category",
            "data": chart_data['Month'].tolist(),
            "name": "月份"
        },
        "yAxis": {
            "type": "value",
            "name": "地震次數"
        },
        "series": [{
            "name": "地震次數",
            "type": "line",
            "data": chart_data['Counts'].tolist(),
            "smooth": True
        }]
    }

    # Display the ECharts chart
    st_echarts(options=echart_option, height="400px")
