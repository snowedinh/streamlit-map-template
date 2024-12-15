import streamlit as st
import pandas as pd

# 设置页面布局
st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)
logo = "地震.png"
st.sidebar.image(logo)

st.title("地震數據的瀏覽與查詢")

# 加载数据的函数
@st.cache_data
def load_data(file_path):
    """
    加载 CSV 文件，并尝试多种编码格式。
    """
    try:
        return pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
    except UnicodeDecodeError:
        try:
            return pd.read_csv(file_path, encoding="gbk", on_bad_lines="skip")
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding="latin1", on_bad_lines="skip")

# 加载数据
file_path = "四川省三级以上地震信息_0.csv"  # 确保路径正确
data = load_data(file_path)

# 检查数据结构
st.write("原始數據的瀏覽：")

# 显示整个表格并启用滚动条
st.dataframe(data, height=500)  # 设置height参数来控制表格的显示高度，超出部分会自动出现滚动条

# 获取四川所有市级城市的名称（假设“Location”列包含市级名称）
city_names = sorted(data['Location'].unique())

# 搜索功能
st.title("搜索功能")
search_city = st.text_input("請輸入縣市的名稱進行查詢", "")

# 下拉选择城市
selected_city = st.selectbox("選擇四川的縣市", city_names)

if search_city:
    filtered_data = data[data["Location"].str.contains(search_city, na=False)]
    if filtered_data.empty:
        st.warning(f"没有找到包含 '{search_city}' 的记录。")
    else:
        st.write(f"以下是包含 '{search_city}' 的地震数据：")
        st.dataframe(filtered_data.style.set_properties(**{
            "border": "1px solid black",
            "color": "black",
            "text-align": "center",
        }))
elif selected_city != "请选择城市":
    filtered_data = data[data["Location"] == selected_city]
    if filtered_data.empty:
        st.warning(f"没有找到关于 '{selected_city}' 的记录。")
    else:
        st.write(f"以下是 '{selected_city}' 的地震数据：")
        st.dataframe(filtered_data.style.set_properties(**{
            "border": "1px solid black",
            "color": "black",
            "text-align": "center",
        }))
else:
    st.write("搜索或选择城市名称进行查看地震记录。")

# 显示数据总览
st.sidebar.write("数据总览")
st.sidebar.write(f"总记录数：{len(data)}")
st.sidebar.write(f"包含城市：{data['Location'].nunique()}")
