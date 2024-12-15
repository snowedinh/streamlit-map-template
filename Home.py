import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")


# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震可视化系统")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo))

# Customize page title
st.title("四川省規模3.0以上地震視覺化網站")

st.markdown(
    """
    準備寫
    """
)

st.header("app應用背景")

markdown = """
準備寫

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
