import streamlit as st
import leafmap.foliumap as leafmap

# 设置页面配置，必须在最开始调用
st.set_page_config(layout="wide")

# 自定义侧边栏
markdown = """
数据来源：https://www.scdata.net.cn/oportal/catalog/5a1b7c017a714f9bb97dfba6d5906fd7
"""

st.sidebar.title("四川地震視覺化系統")
st.sidebar.info(markdown)

# 使用正确的 logo 图片链接
logo = "https://github.com/snowedinh/streamlit-map-template/raw/main/%E5%9C%B0%E9%9C%87.png"
st.sidebar.image(logo)

# 自定义页面标题
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

st.header("app應用功能詳情")

# 功能说明的字典
features = {
    "地震数据搜索": "用户可以通过输入查询的城市名称来筛选地震记录，帮助用户快速筛选出符合条件的地震事件。",
    "震源点的聚合显示": "通过将地图上标记震源点的位置，并根据地震的分布密度自动生成叢集标记。帮助用户更直观地了解震源点的空间分布。",
    "热力图": "直观反映地震事件的密集区域，帮助用户快速识别地震高发地带。",
    "3D与图表统计": "结合地理坐标和震级信息，以高度直观的三维效果、可旋转的动态效果，为用户提供深层次的视觉化感受。图表统计按月份为单位筛选地震事件，能够反映时间尺度上的地震分布情况。",
    "动态缓冲区分析": "帮助用户直观了解地震震源影响范围，通过动态观察不同震源的交叉区域，识别高风险的重叠区域。",
    "標準差分佈":"對監測站點數據和地震震源的點分佈進行度量分析，通過對比標準差橢圓的關鍵指標來分析監測站與震源位置是否具有分佈特征",
}

# 循环生成气泡样式的可展开详情框
for title, description in features.items():
    with st.expander(f"**{title}**", expanded=False):
        st.write(description)
