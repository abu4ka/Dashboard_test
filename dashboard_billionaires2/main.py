import yfinance as yf 
import pandas as pd 
import numpy as np
import streamlit as st 
import plotly.express as px 
import plost
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as  f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def billionaires_dashboard():

    st.sidebar.header('Dashboard Abdurakhmon')

    data = pd.read_csv('World_Billionaire_2024.csv')

    net_worth = data['NET WORTH'].dropna()
    # company_filtered = data['COMPANY']
    # print(net_worth)

    def convert(value):
        try:
            value = value.replace('$', '').replace('B', '').strip()
            return float(value)
        except ValueError:
            return None
    net_worth = net_worth.apply(convert)

    min_value = net_worth.min()
    max_value = net_worth.max()

    min_net_worth, max_net_worth = st.sidebar.slider('Выбери в районе Миллиард', min_value, max_value, (min_value, max_value))
    filtered_data = data[net_worth.between(min_net_worth, max_net_worth)]
    # st.dataframe(filtered_data)
  


    rank = data['RANK'].tolist()
    selected_rank = st.sidebar.selectbox('Выберите место в топе', rank)
    rank_data = data[data['RANK'] == selected_rank]

    company_info = rank_data.iloc[0]['COMPANY']
    executive_name = rank_data.iloc[0]['EXECUTIVE NAME']
    rank = rank_data.iloc[0]['RANK']
    worth = rank_data.iloc[0]['NET WORTH']
    st.header('Информация о компании')
    st.write(f'Выбранная компания: {company_info}, Владелец: {executive_name}, Место в топе: {rank}, Состояние: {worth}')

    st.subheader('Bar plot')
    fig = px.bar(
        data,
        x=['Компания', 'Имя владельца', 'Рейтинг', 'Состояние'],
        y=[company_info, executive_name, rank, worth],
        labels={'x': 'Информация', 'y': 'Показатели'},
        title=f'Информация о компании {company_info}',
        color = ['Компания', 'Имя владельца', 'Рейтинг', 'Состояние'],
        
        )
    
    st.plotly_chart(fig, use_container_width=True)
  
    st.markdown('### Donut Chart')
    donut_theta = st.sidebar.selectbox('Выберите параметр для значений графика', ['RANK', 'COMPANY'])
    donut_labels = st.sidebar.selectbox('Выберите параметр для ', ['NET WORTH', 'EXECUTIVE NAME'])
    filtered_data_for_donut = data.head(10)


    fig_pie = px.pie(
        filtered_data_for_donut,
        values=donut_theta,
        names=donut_labels,
        title='Информация о топ 10 миллиардеров: '
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('### Line Chart')
    fig_line = px.line(
        filtered_data,
        x='COMPANY',
        y='NET WORTH',
        labels={'COMPANY': 'Компания', 'NET WORTH': 'Состояние'},
        title='Состояние компаний'
    )
    st.plotly_chart(fig_line, use_container_width=True)
  


 
    


if __name__ == '__main__':
    billionaires_dashboard()