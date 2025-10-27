"""
View_data_page.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path 

def View_data_file():
    st.markdown('<span class="arrow">➤ View data</span> <p class="font"></p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 Positive & Negative & Health", "🗃 Positive & Negative", "📑 Positive & Health"])
    # 定义固定文件路径（请根据实际情况修改这些路径）
    path_PNH = r'Pertussis data consolidation/Positive, negative, physical examination.xlsx' 
    path_PN = r'Pertussis data consolidation/positive and negative.xlsx' 
    path_PH = r'Pertussis data consolidation/positive and physical examination.xlsx' 
 
    try:
        # 读取第一个表格数据 
        try:
            data_PNH = pd.read_excel(path_PNH) 
        except Exception as e:
            st.error(f" 读取文件失败: {path_PNH}\n错误信息: {str(e)}")
            data_PNH = pd.DataFrame()  # 创建空DataFrame 
 
        # 读取第二个表格数据 
        try:
            data_PN = pd.read_excel(path_PN) 
        except Exception as e:
            st.error(f" 读取文件失败: {path_PN}\n错误信息: {str(e)}")
            data_PN = pd.DataFrame()  # 创建空DataFrame 
 
        # 读取第三个表格数据 
        try:
            data_PH = pd.read_excel(path_PH) 
        except Exception as e:
            st.error(f" 读取文件失败: {path_PH}\n错误信息: {str(e)}")
            data_PH = pd.DataFrame()  # 创建空DataFrame 
 
        # 显示表格数据（按照您要求的格式）
        tab3.dataframe(data_PH,  width=1400, height=710)
        tab2.dataframe(data_PN,  width=1400, height=710)
        tab1.dataframe(data_PNH,  width=1400, height=710)
 
    except Exception as e:
        st.error(f" 初始化页面时发生错误: {str(e)}")











