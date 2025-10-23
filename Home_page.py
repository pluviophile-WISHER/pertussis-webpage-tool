"""
Home_page.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

def Home_file():
    st.markdown('<span class="arrow">➤ Homepage</span> <p class="font"></p>', unsafe_allow_html=True)
    image = Image.open(r'Pertussis data consolidation/pertussis.png')
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(image, caption='Pertussis - Whooping Cough', use_column_width=True)

    with col2:
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

    col3, col4 = st.columns([1, 1])

    with col3:
        labels = ['Infants <1 year', 'Children 5-9 years', 'Children and Adults ≥10 years']
        sizes = [52.40, 13.01, 2.49] 
        sizes.append(100 - sum(sizes)) 
        labels.append('Others') 
        
        colors = ['#00A8C1', '#33B2C7', '#66BCCB', '#99D5D3'] 

        plt.clf() 
        
        plt.figure(figsize=(10, 6)) 
        wedges, texts, autotexts = plt.pie(sizes, colors=colors, autopct='%1.2f%%', startangle=140, pctdistance=0.85)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle) 

        plt.title('Distribution of Pertussis Incidence in China (2018-2022)', fontsize=16)

        plt.legend(wedges, labels, title='Age Groups', loc='center left', bbox_to_anchor=(0.79, 0.5))

        plt.axis('equal')
        st.pyplot(plt)

    with col4:
        months = ['2022-09', '2022-10', '2022-11', '2022-12', '2023-01', 
                  '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', 
                  '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', 
                  '2023-12', '2024-01', '2024-02']
        cases = [3800, 2500, 2010, 1500, 1000, 
                 800, 600, 700, 850, 1030, 
                 2800, 4500, 4800, 5200, 7000, 
                 8500, 14000, 18000]

        plt.clf() 
        
        plt.figure(figsize=(12, 6))
        base_color = '#00A8C1'
        lighter_color = '#93D3D7'
        colors = [lighter_color if i < len(cases) - 1 else base_color for i in range(len(cases))]
        
        plt.bar(months, cases, color=colors)
        plt.title('Trends in Pertussis Cases (September 2022 to February 2024)')
        plt.xlabel('Months')
        plt.ylabel('Number of Cases')
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(plt) 
    
    st.markdown("##### Feedback")
    feedback = st.text_area("Please enter your feedback here:", height=30)


    if st.button("Submit"):
        if feedback:
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please provide feedback")

if __name__ == "__main__":
    Home_file()


