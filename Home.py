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
    本網站基於2019年四川省的地震規模超過3.0的地震數據，使用戶可以直觀地獲取地震發生的時間、空間、規模等信息，為地震的預警與信息收集提供了支持，有助於：
1地震風險評估：使用者可以通過多樣化的地震數據圖表快速了解地震多發區域，結合地理空間分佈特徵，準確識別高風險地區，為抗震設計和防災規劃提供重要依據。
2地震災害預警：通過統計分析歷史地震數據的規模和頻率，結合時間和空間分佈規律，幫助專業機構進行地震預測和災害應急部署，提高社會對地震災害的應對能力。
3公共安全意識提升：借助直觀的數據可視化，讓公眾能更清晰地認識地震的影響範圍，並在日常生活中提升防震意識，為震後救援和重建提供社會支持。
4科學研究與教育：平臺提供的可視化工具和豐富的數據資源，為地震學者提供了便捷的研究平台，同時也是地震相關知識普及和教育的重要工具。
 本網站旨在將專業的地震數據通過友好的交互設計和高效的可視化方式呈現，成為具有實際指導價值的圖形化信息庫。


    """
)

st.header("app應用背景")

markdown = """


"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
