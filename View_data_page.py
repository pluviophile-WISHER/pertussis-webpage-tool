"""
View_data_page.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path  # 必须添加，否则 Path 未定义 

def View_data_file():
    st.markdown('<span class="arrow">➤ View data</span> <p class="font"></p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 Positive & Negative & Health", "🗃 Positive & Negative", "📑 Positive & Health"])
    path_PNH = r'Pertussis data consolidation/positive, negative, physical examination.xlsx'  
    data_PNH = pd.read_excel(path_PNH)
    tab1.dataframe(data_PNH, width=1400, height=710) 

    path_PN = r'Pertussis data consolidation/positive and negative.xlsx'
    data_PN = pd.read_excel(path_PN)
    tab2.dataframe(data_PN, width=1400, height=710)
    
    path_PH = r'Pertussis data consolidation/positive and physical examination.xlsx'
    data_PH = pd.read_excel(path_PH)
    tab3.dataframe(data_PH, width=1400, height=710)





