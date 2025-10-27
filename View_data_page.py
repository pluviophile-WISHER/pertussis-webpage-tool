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
    fixed_path_PNH = r'Pertussis data consolidation/positive negative physical examination.xlsx' 
    fixed_path_PN = r'Pertussis data consolidation/positive and negative.xlsx' 
    fixed_path_PH = r'Pertussis data consolidation/positive and physical examination.xlsx' 
 
    try:
        # 第一个表格：Positive & Negative & Health 
        with tab1:
            try:
                data_PNH = pd.read_excel(fixed_path_PNH) 
                #st.success(f" 成功读取文件: {fixed_path_PNH}")
                st.dataframe(data_PNH,  width=1400, height=710)
            except Exception as e:
                st.error(f" 读取文件失败: {fixed_path_PNH}\n错误信息: {str(e)}")
                st.dataframe(pd.DataFrame(),  width=1400, height=710)  # 显示空表格 
 
        # 第二个表格：Positive & Negative 
        with tab2:
            try:
                data_PN = pd.read_excel(fixed_path_PN) 
                #st.success(f" 成功读取文件: {fixed_path_PN}")
                st.dataframe(data_PN,  width=1400, height=710)
            except Exception as e:
                st.error(f" 读取文件失败: {fixed_path_PN}\n错误信息: {str(e)}")
                st.dataframe(pd.DataFrame(),  width=1400, height=710)  # 显示空表格 
 
        # 第三个表格：Positive & Health 
        with tab3:
            try:
                data_PH = pd.read_excel(fixed_path_PH) 
                #st.success(f" 成功读取文件: {fixed_path_PH}")
                st.dataframe(data_PH,  width=1400, height=710)
            except Exception as e:
                st.error(f" 读取文件失败: {fixed_path_PH}\n错误信息: {str(e)}")
                st.dataframe(pd.DataFrame(),  width=1400, height=710)  # 显示空表格 
 
    except Exception as e:
        st.error(f" 初始化页面时发生错误: {str(e)}")







