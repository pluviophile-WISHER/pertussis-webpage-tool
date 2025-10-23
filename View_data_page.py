"""
View_data_page.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path 

def View_data_file():
    st.markdown('<span class="arrow">➤ View data</span> <p class="font"></p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 Positive & Negative & Health", "🗃 Positive & Negative", "📑 Positive & Health"])
    current_dir = Path(__file__).parent 
    data_folder = current_dir
    

    try: 
        path_PNH = data_folder / "positive, negative, physical examination.xlsx"  
        data_PNH = pd.read_excel(path_PNH)  
        tab1.dataframe(data_PNH,  width=1400, height=710) 
        
        path_PN = data_folder / "positive and negative.xlsx"  
        data_PN = pd.read_excel(path_PN)  
        tab2.dataframe(data_PN,  width=1400, height=710) 
        
        path_PH = data_folder / "positive and physical examination.xlsx"  
        data_PH = pd.read_excel(path_PH)  
        tab3.dataframe(data_PH,  width=1400, height=710) 
        
    except FileNotFoundError as e: 
        st.error(f" 文件未找到：{e}") 
        st.info(" 请检查数据文件夹名称和Excel文件名是否正确，且已上传到项目根目录。") 
    except Exception as e: 
        st.error(f" 读取文件时出错：{e}") 

