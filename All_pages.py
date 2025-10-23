"""
All_pages.py
"""

import streamlit as st
from streamlit_option_menu import option_menu
import Home_page
import View_data_page
import Add_data_page


with st.sidebar:
    menu = ["Homepage", "View data", "Add data"]
    selected = option_menu(menu_title="        Menu", options=menu,
                         icons=['house', 'person', 'file-plus'],
                         menu_icon="list", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "gray", "font-size": "18px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#00A8C1", "font-weight": "normal"},  
    })

if selected == "Homepage":
    Home_page.Home_file()
elif selected == "View data":
    View_data_page.View_data_file()
elif selected == "Add data":
    Add_data_page.Add_data_file()


