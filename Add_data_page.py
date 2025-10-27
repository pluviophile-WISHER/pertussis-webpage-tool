"""
Add_data_page.py
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from joblib import load
from pathlib import Path

def Add_data_file():
    st.markdown('<span class="arrow">➤ Add data</span> <p class="font"></p>', unsafe_allow_html=True)
    
    if "show_data" not in st.session_state:
        st.session_state.show_data = False

    with st.container():
        selected_option = option_menu("Diagnosis results", ["Positive & Negative", "Positive & Health"],
                                        icons=['boxes', 'amd'],
                                        menu_icon="broadcast", default_index=0,
                                        orientation="horizontal",
                                    styles={
                                        "container": {"text-align": "center", "background-color": "#A8D8E5"},
                                        "icon": {"color": "#000000"}, 
                                        "nav-link": {"background-color": "#A8D8E5", "color": "#000000", "padding": "10px 15px"},
                                        "nav-link-selected": {"background-color": "#00A8C1", "color": "white"}, 
                                    }) 

    if selected_option == "Positive & Negative":
    
        input_cols = st.columns(4)
        indicators = [
            "Baso#", "Baso%", "Eos#", "Eos%",
            "Hb", "Hct", "Lymph#", "Lymph%",
            "MCH", "MCHC", "MCV", "MPV",
            "Mono#", "Mono%", "Neut#", "Neut%",
            "P-LCR", "PCT", "PDW", "PLT",
            "RBC", "RDW-CV", "WBC", "CRP"
        ]
        initial_values = [
            0.01, 0.1, 0.67, 6.4,
            111, 33.8, 6.09, 58.4,
            25, 328, 76.3, 7.1,
            0.55, 5.3, 3.11, 29.8,
            8.1, 0.29, 15.2, 411,
            4.43, 12.9, 10.43, 0.28
        ]

        user_input = []
        for index, indicator in enumerate(indicators):
            with input_cols[index % 4]: 
                user_input.append(st.number_input(f"{indicator}：", value=initial_values[index])) 
        
            if (index + 1) % 4 == 0:
                input_cols = st.columns(4)
        
        table_data = {
            "item": indicators,
            "value": user_input,
        }
        
        formatted_table_data = []
        for i in range(0, len(table_data["item"]), 4):
            row = []
            for j in range(4):
                if i + j < len(table_data["item"]):
                    row.append(table_data["item"][i + j])
                    row.append(table_data["value"][i + j])
            formatted_table_data.append(row)
        
        df = pd.DataFrame(formatted_table_data, columns=["item 1", "value 1", "item 2", "value 2", "item 3", "value 3", "item 4", "value 4"])
        
        
        st.markdown("""
        <style>
            .dataframe {
                border: 2px solid black; /* 加粗外框 */
                border-collapse: collapse;
                width: 100%; /* 表格宽度 */
            }
            .dataframe th, .dataframe td {
                text-align: center; /* 数据居中 */
                padding: 8px; /* 内边距 */
            }
            .dataframe tr:nth-child(even) {
                background-color: #f2f2f2; /* 白灰相间 */
            }
        </style>
        """, unsafe_allow_html=True)
        

        if 'show_data' not in st.session_state:
            st.session_state.show_data = False
        if 'show_diagnostic_results' not in st.session_state:
            st.session_state.show_diagnostic_results = False
        if 'show_interpretation' not in st.session_state:
            st.session_state.show_interpretation = False
        
        col11, col22, col33 = st.columns(3)
        
        
        with col11:
            if st.button("View data", key='col11'):
                st.session_state.show_data = not st.session_state.show_data 
                st.session_state.show_diagnostic_results = False 
                st.session_state.show_interpretation = False 
        
        if st.session_state.show_data:
            st.write(df.to_html(classes='dataframe', index=False, escape=False), unsafe_allow_html=True)
            
        try:
            model_path = r"Pertussis data consolidation/PN_CatBoost_model.joblib"  
            model = load(model_path)
        except Exception as e:
            model = None
            st.error(f"{str(e)}")


        
        @st.dialog("Results Form")
        def predict_dialog():
            input_data = [user_input]
            prediction = model.predict(input_data) 
            result = "Pertussis(Positive)" if prediction[0] == 1 else "Pertussis(Negative)"
            try:
                PN_path =r"Pertussis data consolidation/PN.parquet"
                merged_df = pd.read_parquet(PN_path) 
            except Exception as e:
                merged_df = pd.DataFrame()
                st.error(f"{str(e)}") 
            if not merged_df.empty:
                match_row = merged_df[(merged_df['Neut#'] == user_input[14]) & (merged_df['WBC'] == user_input[22])]
                
                if not match_row.empty:
                    report_data = {
                        "Inspection Order ID": [match_row.iloc[0]['Inspection Order ID']], 
                        "Gender": [match_row.iloc[0]['Gender']],
                        "Age": [match_row.iloc[0]['Age']],
                        "Class": [result],
                    }

                    report_df = pd.DataFrame(report_data)

                    st.markdown("<h4 style='text-align: center;'>Hospital Clinical Diagnosis Report</h4>", unsafe_allow_html=True)
        
                    st.write(report_df.to_html(index=False, escape=False), unsafe_allow_html=True)
                    
                    st.write("")
                    st.write("Diagnosis：", result)
        
                    col1, col2, col3, col4 = st.columns(4) 
        
                    with col1:
                        confirm_button = st.button("Confirm", key="confirm_button") 
        
                    with col4:
                        cancel_button = st.button("Cancel", key="cancel_button") 
        
                    if confirm_button:
                        st.write("You have confirmed the operation.")
        
                    if cancel_button:
                        st.write("You have canceled the operation.")
                else:
                    st.write("No matching data.")
            else:
                st.write("No matching data.")
        
        with col22:
            if st.button("View diagnostic results", key='col22'):
                st.session_state.show_diagnostic_results = True 
                st.session_state.show_data = False 
                st.session_state.show_interpretation = False 
                predict_dialog()
                

        normal_ranges = {
            "Baso#": (0.00, 0.10),
            "Baso%": (0, 1),
            "Eos#": (0.00, 0.68),
            "Eos%": (0.0, 9.0),
            "Hb": (107, 141),
            "Hct": (32, 42),
            "Lymph#": (2.4, 8.7),
            "Lymph%": (33, 77),
            "MCH": (24, 30),
            "MCHC": (310, 355),
            "MCV": (72, 86),
            "MPV": (8, 17.1),
            "Mono#": (0.18, 1.13),
            "Mono%": (2, 13),
            "Neut#": (0.8, 5.8),
            "Neut%": (15, 55),
            "P-LCR": (17.5, 42.3),
            "PCT": (0.1, 0.5),
            "PDW": (10, 18),
            "PLT": (190, 524),
            "RBC": (4.0, 5.5),
            "RDW-CV": (11, 16),
            "WBC": (5.1, 14.1),
            "CRP": (0, 6)
        }
        
        def create_explanation_table():
            data = []
            units = {   
                "Baso#": "×10^9/L",
                "Baso%": "%",
                "Eos#": "×10^9/L",
                "Eos%": "%",
                "Hb": "g/L",
                "Hct": "%",
                "Lymph#": "×10^9/L",
                "Lymph%": "%",
                "MCH": "pg",
                "MCHC": "g/L",
                "MCV": "fL",
                "MPV": "fL",
                "Mono#": "×10^9/L",
                "Mono%": "%",
                "Neut#": "×10^9/L",
                "Neut%": "%",
                "P-LCR": "%",
                "PCT": "%",
                "PDW": "%",
                "PLT": "×10^9/L",
                "RBC": "×10^12/L",
                "RDW-CV": "%",
                "WBC": "×10^9/L",
                "CRP": "mg/L"
            }
            
            for i in range(len(indicators)):
                indicator = indicators[i]
                value = initial_values[i]
                normal_min, normal_max = normal_ranges[indicator]
                unit = units.get(indicator, "") 
                
        
                status = "normal" if normal_min <= value <= normal_max else "abnormal"
                data.append({
                    "Indicators": indicator,
                    "Units": unit,
                    "Test values": value,
                    "Reference values": f"{normal_min}-{normal_max}",
                    "Statuses": status
                })
        
            df = pd.DataFrame(data)
            return df
        
        
            st.markdown("<h4 style='color: rgb(0, 168, 193); font-size: 35px;'>Analysis of blood routine test indicators</h4>", unsafe_allow_html=True)
        
            df = create_explanation_table()
            st.markdown("<h2 style='color: rgb(0, 168, 193); font-size: 25px;'>Indicator Explanation</h2>", unsafe_allow_html=True)


    elif selected_option == "Positive & Health":
        input_cols = st.columns(4)
        indicators = [
            "Baso#", "Baso%", "Eos#", "Eos%",
            "Hb", "Hct", "Lymph#", "Lymph%",
            "MCH", "MCHC", "MCV", "MPV",
            "Mono#", "Mono%", "Neut#", "Neut%",
            "P-LCR", "PCT", "PDW", "PLT",
            "RBC", "RDW-CV", "WBC", "CRP"
        ]
        
        initial_values = [
            0, 0, 0.16, 2.3,
            141, 42.1, 3.42, 49,
            27.4, 335, 81.9, 10.4,
            0.86, 12.3, 2.54072, 36.4,
            27.3, 0.26, 11, 254,
            5.14, 13, 6.98, 0.55
        ]

        user_input = []
        
        for index, indicator in enumerate(indicators):
            with input_cols[index % 4]: 
                user_input.append(st.number_input(f"{indicator}：", value=initial_values[index])) 
        
            if (index + 1) % 4 == 0:
                input_cols = st.columns(4)

        table_data = {
            "item": indicators,
            "value": user_input
        }
        
        formatted_table_data = []
        for i in range(0, len(table_data["item"]), 4):
            row = []
            for j in range(4):
                if i + j < len(table_data["item"]):
                    row.append(table_data["item"][i + j])
                    row.append(table_data["value"][i + j])
            formatted_table_data.append(row)
        
        df = pd.DataFrame(formatted_table_data, columns=["item 1", "value 1", "item 2", "value 2", "item 3", "value 3", "item 4", "value 4"])
        
        st.markdown("""
        <style>
            .dataframe {
                border: 2px solid black; /* 加粗外框 */
                border-collapse: collapse;
                width: 100%; /* 表格宽度 */
            }
            .dataframe th, .dataframe td {
                text-align: center; /* 数据居中 */
                padding: 8px; /* 内边距 */
            }
            .dataframe tr:nth-child(even) {
                background-color: #f2f2f2; /* 白灰相间 */
            }
        </style>
        """, unsafe_allow_html=True)
        
        
        if 'show_data' not in st.session_state:
            st.session_state.show_data = False
        if 'show_diagnostic_results' not in st.session_state:
            st.session_state.show_diagnostic_results = False
        if 'show_interpretation' not in st.session_state:
            st.session_state.show_interpretation = False
        
        col11, col22, col33 = st.columns(3)
        
        
        with col11:
            if st.button("View data", key='col11'):
                st.session_state.show_data = not st.session_state.show_data
                st.session_state.show_diagnostic_results = False 
                st.session_state.show_interpretation = False
        
        if st.session_state.show_data:
            st.write(df.to_html(classes='dataframe', index=False, escape=False), unsafe_allow_html=True)
                    
        try:
            model_path_PH = r"Pertussis data consolidation/XGBoost_model.joblib"  
            model_PH = joblib.load(model_path_PH)
        except Exception as e:
            model_PH = None 
            st.error(f"{str(e)}")
        
        st.write("") 
        st.write("")

        
        
        @st.dialog("Results Form")
        def predict_dialog():
            input_data = [user_input] 
            prediction = model_PH.predict(input_data) 
            result = "Pertussis(Positive)" if prediction[0] == 1 else "Pertussis(Health)"
            try:
                PH_path = r"Pertussis data consolidation/PH.parquet"
                merged_df = pd.read_parquet(PH_path)
            except Exception as e:
                merged_df = pd.DataFrame()
                st.error(f"{str(e)}") 

            if not merged_df.empty:
                match_row = merged_df[(merged_df['Neut#'] == user_input[14]) & (merged_df['WBC'] == user_input[22])]
                
                if not match_row.empty:
                    report_data = {
                        "Inspection Order ID": [match_row.iloc[0]['Inspection Order ID']], 
                        "Gender": [match_row.iloc[0]['Gender']],
                        "Age": [match_row.iloc[0]['Age']],
                        "Class": [result],
                    }
                    
                    report_df = pd.DataFrame(report_data)
        
                    st.markdown("<h4 style='text-align: center;'>Hospital Clinical Diagnosis Report</h4>", unsafe_allow_html=True)
        
                    st.write(report_df.to_html(index=False, escape=False), unsafe_allow_html=True)
                    
                    st.write("")
                    st.write("Diagnosis：", result)
        
                    col1, col2, col3, col4 = st.columns(4) 
        
                    with col1:
                        confirm_button = st.button("Confirm", key="confirm_button") 
        
                    with col4:
                        cancel_button = st.button("Cancel", key="cancel_button") 
        
                    if confirm_button:
                        st.write("You have confirmed the operation.")
        
                    if cancel_button:
                        st.write("You have canceled the operation.")
                else:
                    st.write("No matching data.")
            else:
                st.write("No matching data.")
        
        with col22:
            if st.button("View diagnostic results", key='col22'):
                st.session_state.show_diagnostic_results = True 
                st.session_state.show_data = False
                st.session_state.show_interpretation = False 
                predict_dialog()

        normal_ranges = {
            "Baso#": (0.00, 0.10),
            "Baso%": (0, 1),
            "Eos#": (0.00, 0.68),
            "Eos%": (0.0, 9.0),
            "Hb": (107, 141),
            "Hct": (32, 42),
            "Lymph#": (2.4, 8.7),
            "Lymph%": (33, 77),
            "MCH": (24, 30),
            "MCHC": (310, 355),
            "MCV": (72, 86),
            "MPV": (8, 17.1),
            "Mono#": (0.18, 1.13),
            "Mono%": (2, 13),
            "Neut#": (0.8, 5.8),
            "Neut%": (15, 55),
            "P-LCR": (17.5, 42.3),
            "PCT": (0.1, 0.5),
            "PDW": (10, 18),
            "PLT": (190, 524),
            "RBC": (4.0, 5.5),
            "RDW-CV": (11, 16),
            "WBC": (5.1, 14.1),
            "CRP": (0, 6)
        }   
        def create_explanation_table():
            data = []     
            units = {   
                    "Baso#": "×10^9/L",
                    "Baso%": "%",
                    "Eos#": "×10^9/L",
                    "Eos%": "%",
                    "Hb": "g/L",
                    "Hct": "%",
                    "Lymph#": "×10^9/L",
                    "Lymph%": "%",
                    "MCH": "pg",
                    "MCHC": "g/L",
                    "MCV": "fL",
                    "MPV": "fL",
                    "Mono#": "×10^9/L",
                    "Mono%": "%",
                    "Neut#": "×10^9/L",
                    "Neut%": "%",
                    "P-LCR": "%",
                    "PCT": "%",
                    "PDW": "%",
                    "PLT": "×10^9/L",
                    "RBC": "×10^12/L",
                    "RDW-CV": "%",
                    "WBC": "×10^9/L",
                    "CRP": "mg/L"
                }            
            for i in range(len(indicators)):
                indicator = indicators[i]
                value = initial_values[i]
                normal_min, normal_max = normal_ranges[indicator]
                unit = units.get(indicator, "") 
                
        
                status = "normal" if normal_min <= value <= normal_max else "abnormal"
                data.append({
                    "Indicators": indicator,
                    "Units": unit,
                    "Test values": value,
                    "Reference values": f"{normal_min}-{normal_max}",
                    "Statuses": status
                })
        
            df = pd.DataFrame(data)
            return df
        if st.session_state.show_interpretation:   
            st.markdown("<h4 style='color: rgb(0, 168, 193); font-size: 35px;'>Analysis of blood routine test indicators</h4>", unsafe_allow_html=True)






