"""
首页代码：Home_page.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

def Home_file():
    st.markdown('<span class="arrow">➤ Homepage</span> <p class="font"></p>', unsafe_allow_html=True)
    
    # 读取并展示图片
    image = Image.open(r'E:\2025年科研\1月13日\百日咳界面py\pertussis.png')

    # 创建左侧布局
    col1, col2 = st.columns([1, 2])  # 第一列宽度为1，第二列宽度为2
    
    with col1:
        # 在左侧展示图片
        st.image(image, caption='Pertussis - Whooping Cough', use_column_width=True)

    with col2:
        # 输出英文内容
        english_content = """
        Pertussis, commonly known as whooping cough, is a highly contagious bacterial infection primarily affecting the respiratory system. 
        It is caused by Bordetella pertussis, a gram-negative bacterium. The disease is hazardous for infants and young children, who are at
        a higher risk of developing severe complications such as pneumonia, seizures, and even death. However, it can also affect older children
        and adults, though their symptoms may be milder. Pertussis begins with symptoms resembling the common cold, such as a runny nose, low-grade
        fever, and mild cough. As the disease progresses, the characteristic "whooping" sound, which occurs when the patient tries to inhale after 
        a coughing fit, becomes evident. The coughing spells can be violent and exhausting, leading to difficulty breathing, vomiting, and extreme fatigue.
        
        The infection spreads easily through respiratory droplets, meaning that it can be transmitted when an infected person coughs, sneezes,
        or even talks. Close contact with an infected individual, such as in households, schools, and daycare centers, significantly increases 
        the risk of transmission. Vaccination is the most effective means of prevention, with the DTaP vaccine (diphtheria, tetanus, and acellular 
        pertussis) recommended for infants, children, and pregnant women. Booster doses are also advised for adolescents and adults to maintain
        immunity and prevent outbreaks. Despite the availability of a vaccine, pertussis continues to occur worldwide, with occasional outbreaks 
        in both developed and developing countries, underscoring the importance of vaccination and early detection to control its spread.
        """
        st.markdown(english_content)

    # 创建新一排布局用于环形图
    col3, col4 = st.columns([1, 1])  # 第一列宽度为2，第二列宽度为1

    with col3:
        # 生成环形图数据
        labels = ['Infants <1 year', 'Children 5-9 years', 'Children and Adults ≥10 years']
        sizes = [52.40, 13.01, 2.49]  # Percentage data
        sizes.append(100 - sum(sizes))  # Calculate the percentage for 'Others'
        labels.append('Others')  # Add 'Others' label
        
        # Define a custom color palette with different shades of blue
        colors = ['#00A8C1', '#33B2C7', '#66BCCB', '#99D5D3'] 

        # 清除当前的图形
        plt.clf()  # Clear previous figures
        
        # 绘制环形图
        plt.figure(figsize=(10, 6))  # Set the figure size
        wedges, texts, autotexts = plt.pie(sizes, colors=colors, autopct='%1.2f%%', startangle=140, pctdistance=0.85)

        # 添加中央圆形以创建环形图效果
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')  # Create a white circle
        fig = plt.gcf()  # Get the current figure
        fig.gca().add_artist(centre_circle)  # Add the white circle to the figure

        # 设置图表标题
        plt.title('Distribution of Pertussis Incidence in China (2018-2022)', fontsize=16)

        # 添加右侧居中的图例
        plt.legend(wedges, labels, title='Age Groups', loc='center left', bbox_to_anchor=(0.79, 0.5))

        # 显示图形
        plt.axis('equal')  # Ensure the pie chart is a perfect circle
        st.pyplot(plt)  # Use Streamlit's method to display the plot

    with col4:
        # 柱状图数据
        months = ['2022-09', '2022-10', '2022-11', '2022-12', '2023-01', 
                  '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', 
                  '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', 
                  '2023-12', '2024-01', '2024-02']
        cases = [3800, 2500, 2010, 1500, 1000, 
                 800, 600, 700, 850, 1030, 
                 2800, 4500, 4800, 5200, 7000, 
                 8500, 14000, 18000]

        # 清除当前的图形
        plt.clf()  # Clear previous figures
        
        plt.figure(figsize=(12, 6))
        # 定义颜色渐变（由浅到深）
        base_color = '#00A8C1'
        lighter_color = '#93D3D7'  # 浅蓝绿色
        colors = [lighter_color if i < len(cases) - 1 else base_color for i in range(len(cases))]
        
        plt.bar(months, cases, color=colors)
        plt.title('Trends in Pertussis Cases (September 2022 to February 2024)')
        plt.xlabel('Months')
        plt.ylabel('Number of Cases')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 显示柱状图
        st.pyplot(plt)  # Use Streamlit's method to display the plot
    
    
    
    # with feedback_col1:
    st.markdown("##### Feedback")  # 反馈标题
    feedback = st.text_area("Please enter your feedback here:", height=30)  # 设置高度为 30 像素

# with feedback_col2:
#     # 可以在此处放置其他内容或进行调整
#     pass

    if st.button("Submit"):
        if feedback:
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please provide feedback")

# 调用函数以显示内容
if __name__ == "__main__":
    Home_file()
