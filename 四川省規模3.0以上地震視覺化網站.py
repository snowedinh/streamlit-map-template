import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
數據來源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川規模3.0以上地震視覺化網站")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo)

# Customize page title
st.title("Streamlit for Geospatial Applications")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/opengeos/streamlit-map-template).
    """
)

st.header("Instructions")

markdown = """
1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
