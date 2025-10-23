"""
View_data_page.py
"""

import streamlit as st
import pandas as pd


def View_data_file():
    st.markdown('<span class="arrow">➤ View data</span> <p class="font"></p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 Positive & Negative & Health", "🗃 Positive & Negative", "📑 Positive & Health"])
    # 获取当前脚本所在目录的绝对路径 
    current_dir = Path(__file__).parent  # __file__ 是当前脚本的路径 
    # 拼接数据文件夹的绝对路径（确保与实际文件夹名称一致） 
    data_folder = current_dir / "Pertussis data consolidation"  # 注意文件夹名称是否有空格或特殊字符 
    
    # 读取文件（使用绝对路径） 
    try: 
        # 第一个文件 
        path_PNH = data_folder / "positive, negative, physical examination.xlsx"  
        data_PNH = pd.read_excel(path_PNH)  
        tab1.dataframe(data_PNH,  width=1400, height=710) 
        
        # 第二个文件 
        path_PN = data_folder / "positive and negative.xlsx"  
        data_PN = pd.read_excel(path_PN)  
        tab2.dataframe(data_PN,  width=1400, height=710) 
        
        # 第三个文件 
        path_PH = data_folder / "positive and physical examination.xlsx"  
        data_PH = pd.read_excel(path_PH)  
        tab3.dataframe(data_PH,  width=1400, height=710) 
        
    except FileNotFoundError as e: 
        st.error(f" 文件未找到：{e}") 
        st.info(" 请检查数据文件夹名称和Excel文件名是否正确，且已上传到项目根目录。") 
    except Exception as e: 
        st.error(f" 读取文件时出错：{e}") 

