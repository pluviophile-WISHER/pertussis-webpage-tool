"""
View_data_page.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path  # 必须添加，否则 Path 未定义 

def View_data_file():
    st.markdown('<span class="arrow">➤ View data</span> <p class="font"></p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 Positive & Negative & Health", "🗃 Positive & Negative", "📑 Positive & Health"])
    # 获取当前脚本所在目录的绝对路径 
    current_dir = Path(__file__).parent  # __file__ 是当前脚本的路径 
    # 拼接数据文件夹的绝对路径（确保与实际文件夹名称一致） 
    data_folder = current_dir / "Pertussis data consolidation"  # 注意文件夹名称是否有空格或特殊字符 
    
    # 直接指定项目根目录（Streamlit Cloud的根目录） 
    root_dir = "/mount/src/pertussis-webpage-tool"  # 替换为你的项目仓库名 
    data_folder = os.path.join(root_dir,  "Pertussis data consolidation")  # 拼接数据文件夹路径 
    
    # 验证数据文件夹是否存在 
    if not os.path.exists(data_folder):  
        st.error(f" 数据文件夹不存在：{data_folder}") 
        st.info(" 请检查仓库中是否已上传 'Pertussis data consolidation' 文件夹") 
        return 
    
    # 读取文件（带文件名验证） 
    try: 
        # 第一个文件 
        path_PNH = os.path.join(data_folder,  "positive, negative, physical examination.xlsx")  
        if not os.path.exists(path_PNH):  
            st.error(f" 文件不存在：{path_PNH}") 
        else: 
            data_PNH = pd.read_excel(path_PNH)  
            tab1.dataframe(data_PNH,  width=1400, height=710) 
        
        # 第二个文件 
        path_PN = os.path.join(data_folder,  "positive and negative.xlsx")  
        if not os.path.exists(path_PN):  
            st.error(f" 文件不存在：{path_PN}") 
        else: 
            data_PN = pd.read_excel(path_PN)  
            tab2.dataframe(data_PN,  width=1400, height=710) 
        
        # 第三个文件 
        path_PH = os.path.join(data_folder,  "positive and physical examination.xlsx")  
        if not os.path.exists(path_PH):  
            st.error(f" 文件不存在：{path_PH}") 
        else: 
            data_PH = pd.read_excel(path_PH)  
            tab3.dataframe(data_PH,  width=1400, height=710) 
            
    except Exception as e: 
        st.error(f" 读取文件失败：{str(e)}") 



