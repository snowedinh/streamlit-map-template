import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
st.set_page_config(layout="wide")
# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""
st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo)

st.title("熱力圖")

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
        
        # 創建地圖，設置中心為四川
        m = leafmap.Map(center=[30.6, 104.1], zoom=7)
        
        # 添加熱力圖，從 DataFrame 中提取數據
        m.add_heatmap(
            data=df,
            latitude="Lat",    
            longitude="Lon",   
            value="Data",      
            name="Heat map",
            radius=20,
        )

# 將地圖嵌入到 Streamlit 頁面中
m.to_streamlit(height=700)
