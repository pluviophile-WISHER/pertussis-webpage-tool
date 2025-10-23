"""
添加患者代码：Add_data_page.py
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from joblib import load
from openai import OpenAI

def Add_data_file():
    # 添加箭头指示标识
    st.markdown('<span class="arrow">➤ Add data</span> <p class="font"></p>', unsafe_allow_html=True)
    
    # 初始化状态
    if "show_data" not in st.session_state:
        st.session_state.show_data = False

    # 创建一个头部的选项菜单
    with st.container():
        selected_option = option_menu("Diagnosis results", ["Positive & Negative", "Positive & Health"],
                                       icons=['boxes', 'amd'],
                                       menu_icon="broadcast", default_index=0,
                                       orientation="horizontal",  # 水平布局
                                   styles={
                                       "container": {"text-align": "center", "background-color": "#A8D8E5"},  # 浅蓝绿色背景
                                       "icon": {"color": "#000000"},  # 选项图标颜色
                                       "nav-link": {"background-color": "#A8D8E5", "color": "#000000", "padding": "10px 15px"},
                                       "nav-link-selected": {"background-color": "#00A8C1", "color": "white"},  # 深蓝绿色选中的项
                                   })  # 中心对齐


    # 根据选择的选项显示内容
    if selected_option == "Positive & Negative":
        # st.markdown("""<h4 style='text-align: center;'>请输入患者详细信息</h4>""", unsafe_allow_html=True)
    
        # 每行4列
        input_cols = st.columns(4)
        
        # 更新指标及初始值
        indicators = [
            "Baso#", "Baso%", "Eos#", "Eos%",
            "Hb", "Hct", "Lymph#", "Lymph%",
            "MCH", "MCHC", "MCV", "MPV",
            "Mono#", "Mono%", "Neut#", "Neut%",
            "P-LCR", "PCT", "PDW", "PLT",
            "RBC", "RDW-CV", "WBC", "CRP"
        ]
        
        # 更新后的初始值
        initial_values = [
            0.01, 0.1, 0.67, 6.4,
            111, 33.8, 6.09, 58.4,
            25, 328, 76.3, 7.1,
            0.55, 5.3, 3.11, 29.8,
            8.1, 0.29, 15.2, 411,
            4.43, 12.9, 10.43, 0.28
        ]

        # 用户输入数据列表
        user_input = []
        
        # 遍历指标来创建输入框
        for index, indicator in enumerate(indicators):
            with input_cols[index % 4]:  # 每4个一行
                user_input.append(st.number_input(f"{indicator}：", value=initial_values[index]))  # 设置初始值
        
            # 每行结束后切换到下一行
            if (index + 1) % 4 == 0:
                input_cols = st.columns(4)
        
        # 创建表格形式的数据
        table_data = {
            "item": indicators,
            "value": user_input,
        }
        
        # 将表格数据转换为每行包含四个指标及其值
        formatted_table_data = []
        for i in range(0, len(table_data["item"]), 4):
            row = []
            for j in range(4):
                if i + j < len(table_data["item"]):
                    row.append(table_data["item"][i + j])
                    row.append(table_data["value"][i + j])
            formatted_table_data.append(row)
        
        # 创建DataFrame
        df = pd.DataFrame(formatted_table_data, columns=["item 1", "value 1", "item 2", "value 2", "item 3", "value 3", "item 4", "value 4"])
        
        
        # 继续使用原来的样式自定义代码
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
        
        
        
        # 初始化状态
        if 'show_data' not in st.session_state:
            st.session_state.show_data = False
        if 'show_diagnostic_results' not in st.session_state:
            st.session_state.show_diagnostic_results = False
        if 'show_interpretation' not in st.session_state:
            st.session_state.show_interpretation = False
        
        # 展示已选择的数据的按钮和数据表
        col11, col22, col33 = st.columns(3)
        
        
        with col11:
            if st.button("View data", key='col11'):
                st.session_state.show_data = not st.session_state.show_data  # 切换显示状态
                st.session_state.show_diagnostic_results = False  # 清除其他结果状态
                st.session_state.show_interpretation = False  # 清除解读结果状态
        
        if st.session_state.show_data:
            st.write(df.to_html(classes='dataframe', index=False, escape=False), unsafe_allow_html=True)
            

        
        # 加载模型
        model_path = r'E:\2025年科研\1月8日\阳阴-模型保存\CatBoost_model.joblib'
        model = load(model_path)
        
        
        # 添加一些空行以分隔表格和按钮
        # st.write("")  # 添加一行空行
        # st.write("")
        
        



        
        @st.dialog("Results Form")
        def predict_dialog():
            
            # 将用户输入转换为NumPy数组或适当格式进行预测
            input_data = [user_input]  # 根据实际需要调整输入格式
            prediction = model.predict(input_data)  # 进行预测
            # 显示预测结果
            result = "Pertussis(Positive)" if prediction[0] == 1 else "Pertussis(Negative)"

            merged_df = pd.read_excel(r'E:\2025年科研\1月13日\百日咳界面py\百日咳数据合并\修改Gender后-阳阴.xlsx')
        
            # 筛选匹配的行
            if not merged_df.empty:
                # 使用CA125进行匹配和WBC进行匹配
                match_row = merged_df[(merged_df['Neut#'] == user_input[14]) & (merged_df['WBC'] == user_input[22])]
                
                if not match_row.empty:
                    report_data = {
                        "Inspection Order ID": [match_row.iloc[0]['Inspection Order ID']],  # 从匹配行中获得Date值
                        "Gender": [match_row.iloc[0]['Gender']],
                        "Age": [match_row.iloc[0]['Age']],
                        "Class": [result],
                    }
        
                    # 将报告数据转换为DataFrame
                    report_df = pd.DataFrame(report_data)
        
                    # 显示标题
                    st.markdown("<h4 style='text-align: center;'>Hospital Clinical Diagnosis Report</h4>", unsafe_allow_html=True)
        
                    # 使用st.write显示表格
                    st.write(report_df.to_html(index=False, escape=False), unsafe_allow_html=True)
                    
                    st.write("")
                    st.write("Diagnosis：", result)
        
                    # 在表格下面的按钮
                    col1, col2, col3, col4 = st.columns(4)  # 创建两列
        
                    with col1:
                        confirm_button = st.button("Confirm", key="confirm_button")  # 将确认按钮放在左侧
        
                    with col4:
                        cancel_button = st.button("Cancel", key="cancel_button")  # 将取消按钮放在右侧
        
                    if confirm_button:
                        st.write("You have confirmed the operation.")
                        # 此处可添加确认后的操作，比如数据存储等
        
                    if cancel_button:
                        st.write("You have canceled the operation.")
                else:
                    st.write("No matching data.")
            else:
                st.write("No matching data.")
        
        with col22:
        # 主程序启动：当点击“填写信息”按钮时，调用弹出框
            if st.button("View diagnostic results", key='col22'):
                st.session_state.show_diagnostic_results = True  # 设置诊断结果显示状态
                st.session_state.show_data = False  # 清除显示数据状态
                st.session_state.show_interpretation = False  # 清除解读结果状态
                predict_dialog()
                
                
        
        
        # 正常参考范围(准确)
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
                unit = units.get(indicator, "")  # 获取单位，如果没有则默认为空字符串
                
        
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
        
        
        # # 创建深度思考文本
        # def create_thoughts():
        #     # 初始化 OpenAI 客户端（连接到本地 Ollama）
        #     client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="lm-studio")
            
        #     # 用户输入问题
        #     prompt = st.text_input("Please enter your question:", "Please enter...")
            
        #     thoughts = ""  # 初始化 thoughts 变量，确保它有一个初始值
            
        #     if st.button("Generate Answers"):
        #         if prompt:  # 确保问题不为空
        #             try:
        #                 # 调用 Ollama API 生成回答
        #                 completion = client.chat.completions.create(
        #                     model="deepseek-r1:1.5b",  # 替换为你的模型名称
        #                     messages=[{"role": "user", "content": prompt}],
        #                     temperature=0.7,
        #                     max_tokens=512
        #                 )
            
        #                 # 提取生成的回答
        #                 thoughts = completion.choices[0].message.content
                        
        #                 # 去掉回答中的 <think> 标签
        #                 thoughts = thoughts.replace("<think>", "").replace("</think>", "")  
            
        #                 # 在页面上显示问题和回答
        #                 st.markdown("###  Question: ")
        #                 st.write(prompt)
        #                 st.markdown("###  Answer: ")
        #                 st.write(thoughts)
            
        #             except Exception as e:
        #                 st.error(f" Error occurred: {str(e)}")
        #         else:
        #             st.warning("Please enter a question!")

        #     # 返回生成的回答
        #     if thoughts:  # 仅在有生成回答时返回
        #         return st.markdown(thoughts, unsafe_allow_html=True)
        

        # # 存储解读结果
        # if 'show_interpretation' not in st.session_state:
        #     st.session_state.show_interpretation = False
        
        # # 添加按钮以查看指标解读
        # with col33:
        #     if st.button("View indicator interpretation", key='col33'):
        #         st.session_state.show_interpretation = True
        #         st.session_state.show_diagnostic_results = False
        #         st.session_state.show_data = False

        
        
        # if st.session_state.show_interpretation:
        
        # 主函数
        # def main():
            st.markdown("<h4 style='color: rgb(0, 168, 193); font-size: 35px;'>Analysis of blood routine test indicators</h4>", unsafe_allow_html=True)
        
            # 显示指标解释表
            df = create_explanation_table()
            st.markdown("<h2 style='color: rgb(0, 168, 193); font-size: 25px;'>Indicator Explanation</h2>", unsafe_allow_html=True)
            # st.dataframe(df, width=1000, height=500)  # 设置表格宽度
            # st.dataframe(df, column_config={
            #     "Indicators": {"title": "Indicators"},
            #     "Units": {"title": "Units"},
            #     "Test values": {"title": "Test values"},
            #     "Reference values": {"title": "Reference values"},
            #     "Statuses": {"title": "Statuses"}
            # }, height=600)
            
            # 显示深度思考
            # create_thoughts()











        
    elif selected_option == "Positive & Health":
        # 每行4列
        input_cols = st.columns(4)
        
        # 更新指标及初始值
        indicators = [
            "Baso#", "Baso%", "Eos#", "Eos%",
            "Hb", "Hct", "Lymph#", "Lymph%",
            "MCH", "MCHC", "MCV", "MPV",
            "Mono#", "Mono%", "Neut#", "Neut%",
            "P-LCR", "PCT", "PDW", "PLT",
            "RBC", "RDW-CV", "WBC", "CRP"
        ]
        
        # 更新后的初始值
        initial_values = [
            0, 0, 0.16, 2.3,
            141, 42.1, 3.42, 49,
            27.4, 335, 81.9, 10.4,
            0.86, 12.3, 2.54072, 36.4,
            27.3, 0.26, 11, 254,
            5.14, 13, 6.98, 0.55
        ]

        
        # 用户输入数据列表
        user_input = []
        
        # 遍历指标来创建输入框
        for index, indicator in enumerate(indicators):
            with input_cols[index % 4]:  # 每4个一行
                user_input.append(st.number_input(f"{indicator}：", value=initial_values[index]))  # 设置初始值
        
            # 每行结束后切换到下一行
            if (index + 1) % 4 == 0:
                input_cols = st.columns(4)
        
        # 创建表格形式的数据
        table_data = {
            "item": indicators,
            "value": user_input
        }
        
        # 将表格数据转换为每行包含四个指标及其值
        formatted_table_data = []
        for i in range(0, len(table_data["item"]), 4):
            row = []
            for j in range(4):
                if i + j < len(table_data["item"]):
                    row.append(table_data["item"][i + j])
                    row.append(table_data["value"][i + j])
            formatted_table_data.append(row)
        
        # 创建DataFrame
        df = pd.DataFrame(formatted_table_data, columns=["item 1", "value 1", "item 2", "value 2", "item 3", "value 3", "item 4", "value 4"])
        
        # 继续使用原来的样式自定义代码
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
        
        
        # 初始化状态
        if 'show_data' not in st.session_state:
            st.session_state.show_data = False
        if 'show_diagnostic_results' not in st.session_state:
            st.session_state.show_diagnostic_results = False
        if 'show_interpretation' not in st.session_state:
            st.session_state.show_interpretation = False
        
        # 展示已选择的数据的按钮和数据表
        col11, col22, col33 = st.columns(3)
        
        
        with col11:
            if st.button("View data", key='col11'):
                st.session_state.show_data = not st.session_state.show_data  # 切换显示状态
                st.session_state.show_diagnostic_results = False  # 清除其他结果状态
                st.session_state.show_interpretation = False  # 清除解读结果状态
        
        if st.session_state.show_data:
            st.write(df.to_html(classes='dataframe', index=False, escape=False), unsafe_allow_html=True)
                    

        
        
        # 加载模型
        model_path = r'E:\2025年科研\1月8日\阳体-模型保存\GBDT_model.joblib'
        model = load(model_path)
        
        # 添加一些空行以分隔表格和按钮
        st.write("")  # 添加一行空行
        st.write("")

        
        
        @st.dialog("Results Form")
        def predict_dialog():
            # 将用户输入转换为NumPy数组或适当格式进行预测
            input_data = [user_input]  # 根据实际需要调整输入格式
            prediction = model.predict(input_data)  # 进行预测
            # 显示预测结果
            result = "Pertussis(Positive)" if prediction[0] == 1 else "Pertussis(Health)"

            merged_df = pd.read_excel(r'E:\2025年科研\1月13日\百日咳界面py\百日咳数据合并\修改Gender后-阳体.xlsx')

            # 筛选匹配的行
            if not merged_df.empty:
                # 使用CA125进行匹配
                match_row = merged_df[(merged_df['Neut#'] == user_input[14]) & (merged_df['WBC'] == user_input[22])]
                
                if not match_row.empty:
                    report_data = {
                        "Inspection Order ID": [match_row.iloc[0]['Inspection Order ID']],  # 从匹配行中获得Date值
                        "Gender": [match_row.iloc[0]['Gender']],
                        "Age": [match_row.iloc[0]['Age']],
                        "Class": [result],
                    }
                    
                    # 将报告数据转换为DataFrame
                    report_df = pd.DataFrame(report_data)
        
                    # 显示标题
                    st.markdown("<h4 style='text-align: center;'>Hospital Clinical Diagnosis Report</h4>", unsafe_allow_html=True)
        
                    # 使用st.write显示表格
                    st.write(report_df.to_html(index=False, escape=False), unsafe_allow_html=True)
                    
                    st.write("")
                    st.write("Diagnosis：", result)
        
                    # 在表格下面的按钮
                    col1, col2, col3, col4 = st.columns(4)  # 创建两列
        
                    with col1:
                        confirm_button = st.button("Confirm", key="confirm_button")  # 将确认按钮放在左侧
        
                    with col4:
                        cancel_button = st.button("Cancel", key="cancel_button")  # 将取消按钮放在右侧
        
                    if confirm_button:
                        st.write("You have confirmed the operation.")
                        # 此处可添加确认后的操作，比如数据存储等
        
                    if cancel_button:
                        st.write("You have canceled the operation.")
                else:
                    st.write("No matching data.")
            else:
                st.write("No matching data.")
        
        with col22:
        # 主程序启动：当点击“填写信息”按钮时，调用弹出框
            if st.button("View diagnostic results", key='col22'):
                st.session_state.show_diagnostic_results = True  # 设置诊断结果显示状态
                st.session_state.show_data = False  # 清除显示数据状态
                st.session_state.show_interpretation = False  # 清除解读结果状态
                predict_dialog()




        # 正常参考范围(准确)
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
                unit = units.get(indicator, "")  # 获取单位，如果没有则默认为空字符串
                
        
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
        
        
        # 创建深度思考文本
        def create_thoughts():
            # 初始化 OpenAI 客户端（连接到本地 Ollama）
            client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="lm-studio")
            
            # 用户输入问题
            prompt = st.text_input("Please enter your question:", "Please enter...")
            
            thoughts = ""  # 初始化 thoughts 变量，确保它有一个初始值
            
            if st.button("Generate Answers"):
                if prompt:  # 确保问题不为空
                    try:
                        # 调用 Ollama API 生成回答
                        completion = client.chat.completions.create(
                            model="deepseek-r1:1.5b",  # 替换为你的模型名称
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7,
                            max_tokens=512
                        )
            
                        # 提取生成的回答
                        thoughts = completion.choices[0].message.content
                        
                        # 去掉回答中的 <think> 标签
                        thoughts = thoughts.replace("<think>", "").replace("</think>", "")  
            
                        # 在页面上显示问题和回答
                        st.markdown("###  Question: ")
                        st.write(prompt)
                        st.markdown("###  Answer: ")
                        st.write(thoughts)
            
                    except Exception as e:
                        st.error(f" Error occurred: {str(e)}")
                else:
                    st.warning("Please enter a question!")

            # 返回生成的回答
            if thoughts:  # 仅在有生成回答时返回
                return st.markdown(thoughts, unsafe_allow_html=True)
                
        
        
        
        # 存储解读结果
        if 'show_interpretation' not in st.session_state:
            st.session_state.show_interpretation = False
        
        # 添加按钮以查看指标解读
        with col33:
            if st.button("View indicator interpretation", key='col33'):
                st.session_state.show_interpretation = True
                st.session_state.show_diagnostic_results = False
                st.session_state.show_data = False

        
        
        if st.session_state.show_interpretation:
        
        # 主函数
        # def main():
            st.markdown("<h4 style='color: rgb(0, 168, 193); font-size: 35px;'>Analysis of blood routine test indicators</h4>", unsafe_allow_html=True)
        
            # 显示指标解释表
            df = create_explanation_table()
            st.markdown("<h2 style='color: rgb(0, 168, 193); font-size: 25px;'>Indicator Explanation</h2>", unsafe_allow_html=True)
            st.dataframe(df, width=1000, height=500)  # 设置表格宽度
            # st.dataframe(df, column_config={
            #     "Indicators": {"title": "Indicators"},
            #     "Units": {"title": "Units"},
            #     "Test values": {"title": "Test values"},
            #     "Reference values": {"title": "Reference values"},
            #     "Statuses": {"title": "Statuses"}
            # }, height=600)
        
            # 显示深度思考
            create_thoughts()






                
        
        