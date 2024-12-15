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

# Customize page title
st.title("四川省規模3.0以上地震視覺化網站")

st.markdown(
    """
    <div style="background-color: #ffe4e1; padding: 15px; border-radius: 10px; border: 1px solid #f5c2c2;">
        <p style="font-size: 16px; line-height: 1.6;">
            本網站基於2019年四川省的地震規模超過3.0的地震數據，使用戶可以直觀地獲取地震發生的時間、空間、規模等信息，使用者可以通過多樣化的地震數據圖表快速了解地震多發區域，結合地理空間分佈特徵，準確識別高風險地區，為抗震設計和防災規劃提供重要依據。
            <br><br>
            借助直觀的數據可視化，讓公眾能更清晰地認識地震的影響範圍，並在日常生活中提升防震意識，成為地震相關知識普及和教育的重要工具。
            <br><br>
            本網站旨在將專業的地震數據通過友好的交互設計和高效的可視化方式呈現，提供具有實際指導價值的圖形化信息庫。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.header("app應用背景")

markdown = """
功能介紹：1
"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
