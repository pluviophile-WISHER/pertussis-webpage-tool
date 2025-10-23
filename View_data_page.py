# -*- coding: utf-8 -*-
"""
数据查看代码：View_data_page.py
📊🌍
"""

import streamlit as st
import pandas as pd


def View_data_file():
    # 添加箭头指示标识
    st.markdown('<span class="arrow">➤ View data</span> <p class="font"></p>', unsafe_allow_html=True)
    # st.title("Patient data")
    tab1, tab2, tab3 = st.tabs(["📖 Positive & Negative & Health", "🗃 Positive & Negative", "📑 Positive & Health"])
    # tab1, tab2, tab3 = st.tabs(["&#128214; total", "&#128451; male", "&#128209; female"])
    path_PNH = r'E:\2025年科研\1月4日\百日咳数据处理过程\处理后合并-阳阴体.xlsx'  
    data_PNH = pd.read_excel(path_PNH)
    # st.dataframe(data_PNH, width=1000, height=500)  # 设置表格宽度
    # 假设要格式化的列名为 'Date'
    # data_total['Date'] = data_total['Date'].apply(lambda x: '{:.0f}'.format(x))
    # tab1.write(data_PNH, use_container_width=True)
    tab1.dataframe(data_PNH, width=1400, height=710) 

    path_PN = r'E:\2025年科研\1月4日\百日咳数据处理过程\阳性and阴性\merged_百日咳数据-阳性7and阴性7.xlsx'
    data_PN = pd.read_excel(path_PN)
    # tab2.write(data_PN, use_container_width=True)
    tab2.dataframe(data_PN, width=1400, height=710)
    
    path_PH = r'E:\2025年科研\1月4日\百日咳数据处理过程\阳性and体检\merged_百日咳数据-筛选出Class=2and体检5.xlsx'
    data_PH = pd.read_excel(path_PH)
    # tab3.write(data_PH, use_container_width=True)
    tab3.dataframe(data_PH, width=1400, height=710)
