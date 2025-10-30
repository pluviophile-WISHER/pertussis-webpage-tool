"""
View_data_page.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path 

def View_data_file():
    st.markdown('<span class="arrow">➤ View data</span> <p class="font"></p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 Positive & Negative & Health", "🗃 Positive & Negative", "📑 Positive & Health"])
    path_PNH = r'Pertussis data consolidation/Positive, negative, physical examination.xlsx' 
    path_PN = r'Pertussis data consolidation/positive and negative.xlsx' 
    path_PH = r'Pertussis data consolidation/positive and physical examination.xlsx' 
 
    try:
        try:
            data_PNH = pd.read_excel(path_PNH) 
        except Exception as e:
            st.error(f" File reading failed: {path_PNH}\nError message: {str(e)}")
            data_PNH = pd.DataFrame() 
 
        try:
            data_PN = pd.read_excel(path_PN) 
        except Exception as e:
            st.error(f" File reading failed: {path_PN}\nError message: {str(e)}")
            data_PN = pd.DataFrame()
 
        try:
            data_PH = pd.read_excel(path_PH) 
        except Exception as e:
            st.error(f" File reading failed: {path_PH}\nError message: {str(e)}")
            data_PH = pd.DataFrame()
 
        tab3.dataframe(data_PH,  width=1400, height=710)
        tab2.dataframe(data_PN,  width=1400, height=710)
        tab1.dataframe(data_PNH,  width=1400, height=710)
 
    except Exception as e:
        st.error(f" An error occurred when initializing the page: {str(e)}")












