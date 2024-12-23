import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import folium

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""
st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)

# Check if the image exists locally or use an online image URL
logo = "地震.png"  # Local file path (replace with correct path if needed)
try:
    st.sidebar.image(logo)
except:
    st.sidebar.image("https://example.com/path/to/your/image.png")  # Fallback URL

st.title("立体地形图")

with st.expander("See source code"):
    with st.echo():
        filepath = "https://github.com/hjh2003/GIS/raw/refs/heads/main/Sichuan_Earthquakes_3.0_Above.csv"
        
        try:
            df = pd.read_csv(filepath, encoding='gbk')  
        except UnicodeDecodeError:
            st.error("文件編碼錯誤，請檢查文件的編碼格式！")
            st.stop()
        
        # 檢查數據是否正確
        st.write("文件預覽：", df.head())
        
        # 创建地图，设置中心为四川
        m = leafmap.Map(center=[30.6, 104.1], zoom=7)
        
        # 添加地形图层
        # 使用 folium 库中的地形图层（使用OpenTopoMap作为例子）
        folium.TileLayer(
            tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", 
            attr="&copy; OpenTopoMap contributors", 
            name="Topographic Map", 
            overlay=True, 
            control=True
        ).add_to(m)

        # 如果需要显示地震热力图层（如果有的话），可以继续添加热力图层
        m.add_heatmap(
            data=df,
            latitude="Lat",    
            longitude="Lon",   
            value="Data",      
            name="Heat map",
            radius=20,
        )

# 将地图嵌入到 Streamlit 页面中
m.to_streamlit(height=700)
