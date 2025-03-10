import streamlit as st
import pandas as pd  
import numpy as np
import matplotlib.pyplot as pltpip 
import seaborn as sns
from plotly import graph_objs as go
import warnings
warnings.filterwarnings('ignore')

# interactive visualization
import plotly.express as px

cnf, dth, rec, act = '#393e46', '#ff2e63', '#21bf73', '#fe9801' 

df = pd.read_csv("D:\KULIAH\Kasus Covid 19 IDN 2021.csv", parse_dates=['Tanggal'])
#Data Cleaning
df_cleaned = df.dropna(axis=1)
df_cleaned_out = df_cleaned.loc[df["Wilayah"] != "Indonesia" ]

# st.header('This is a header')
# st.markdown('Streamlit is **_really_ cool**.')

options = st.sidebar.radio('Menu', options=['Total Kasus','Tren', 'Peta Persebaran', 'Data Header', 'Data Statistics'])



def stats(dataframe):
    st.title('Data Statistics')
    #Before Data Cleaning
    st.header('Before Data Cleaning')
    st.write(df.shape)
    st.write(dataframe.describe())
    st.markdown("Jumlah Data yang NULL")
    st.write(df.isnull().sum())

    #After Data Cleaning
    st.header('After Data Cleaning')
    st.write(df_cleaned.shape)
    st.write(df_cleaned.describe())
    st.markdown("Jumlah Data yang NULL")
    st.write(df_cleaned.isnull().sum())

def data_header(dataframe):
    st.title('Data Header')
    #Before Data Cleaning
    st.header('Before Data Cleaning')
    st.write(df.shape)
    st.dataframe(df)

    #After Data Cleaning
    st.header('After Data Cleaning')
    st.write(df_cleaned.shape)
    st.dataframe(df_cleaned)

def plot(dataframe):

    # ///////
    st.header("Tren Lonjakan COVID 19 di Indonesia")
    st.write('Pilih Jenis Data:')
    option_1 = st.checkbox('Kasus Harian')
    option_2 = st.checkbox('Sembuh Harian')
    option_3 = st.checkbox('Meninggal Harian')

    fig_main = go.Figure()
    if (option_1 or option_2 or option_3) is False:
        fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Kasus Baru'], name='Kasus Harian'))
        
    else:
        if option_1:
             fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Kasus Baru'], name='Kasus Harian'))
        
        if option_2:
             fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Sembuh'], name='Sembuh Harian'))
        
        if option_3:
             fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Kematian'], name='Meninggal Harian'))
    
    fig_main.layout.update(title_text='Indonesia Covid-19', 
        xaxis_rangeslider_visible=True, 
        hovermode='x',
        legend_orientation='v')

    st.plotly_chart(fig_main, use_container_width=True)

    # ///////
    st.header("Tren Total COVID 19 di Indonesia")
    st.write('Pilih Jenis Data:')
    
    option_1 = st.checkbox('Total Kasus')
    option_2 = st.checkbox('Total Sembuh')
    option_3 = st.checkbox('Total Meninggal')

    fig_main = go.Figure()
    if (option_1 or option_2 or option_3) is False:
        fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Total Kasus Baru'], name='Total Kasus'))
        
    else:
        if option_1:
             fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Total Kasus Baru'], name='Total Kasus'))
        
        if option_2:
             fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Total Sembuh'], name='Total Sembu'))
        
        if option_3:
             fig_main.add_trace(go.Scatter(x=df['Tanggal'], y=df['Total Kematian'], name='Total Meninggal'))
    
    fig_main.layout.update(title_text='Indonesia Covid-19', 
        xaxis_rangeslider_visible=True, 
        hovermode='x',
        legend_orientation='v')

    st.plotly_chart(fig_main, use_container_width=True)
    list = df_cleaned_out['Wilayah'].unique()
    wilayah4 = st.selectbox("Pilih Wilayah:", list)

    temp = df_cleaned_out[df_cleaned_out['Wilayah']==wilayah4].groupby('Tanggal')['Kasus Baru', 'Kematian', 'Sembuh'].sum().reset_index()
    temp = temp.melt(id_vars="Tanggal", value_vars=['Kasus Baru', 'Kematian', 'Sembuh'],
                 var_name='Case', value_name='Count')
    temp.head()

    fig = px.area(temp, x="Tanggal", y="Count", color='Case', height=600, width=700,
             title=wilayah4, color_discrete_sequence = [dth,  cnf, rec, act])
    fig.update_layout(xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    # ///////
    st.header("Tren Lonjakan Kasus Terkonfirmasi Berdasarkan Provinsi")
    list = df_cleaned_out['Wilayah'].unique()
    wilayah = st.selectbox("Pilih Wilayah Total Kasus:", list)

    fig = px.line(df[df['Wilayah'] == wilayah], 
    x = "Tanggal",y = "Kasus Baru", title = wilayah, color_discrete_sequence=[dth])
    st.plotly_chart(fig)

    # ///////
    st.header("Tren Lonjakan Kasus Sembuh Berdasarkan Provinsi")
    wilayah2 = st.selectbox("Pilih Wilayah Sembuh:", list)

    fig = px.line(df[df['Wilayah'] == wilayah2], 
    x = "Tanggal",y = "Sembuh", title = wilayah2, color_discrete_sequence=[rec])
    st.plotly_chart(fig)

    # ///////
    st.header("Tren Lonjakan Kasus Meninggal Berdasarkan Provinsi")
    wilayah3 = st.selectbox("Pilih Wilayah Total Meninggal:", list)

    fig = px.line(df[df['Wilayah'] == wilayah3], 
    x = "Tanggal",y = "Kematian", title = wilayah3, color_discrete_sequence=[cnf])
    st.plotly_chart(fig)

    

def mapping(dataframe):
    # --- Header ---
    st.header("Peta Persebaran Kasus Covid-19 di Indonesia")    
    fig = px.scatter_mapbox(df_cleaned_out, lat="Garis Lintang (lat)", lon="Garis Bujur (lot)", color="Total Kematian", size="Total Kematian",
                        mapbox_style="open-street-map", zoom = 0.5, color_continuous_scale = 'Plasma')
    st.plotly_chart(fig)

    st.header("Laju Persebaran Kasus Covid-19 di Indonesia Berdasarkan Tahun")
    df_cleaned_out['Bulan']=df_cleaned_out['Tanggal'].dt.month
    df_cleaned_out['Tahun']=df_cleaned_out['Tanggal'].dt.year
    
    fig = px.density_mapbox(df_cleaned_out, lat="Garis Lintang (lat)", lon="Garis Bujur (lot)",  z = 'Total Kasus Baru',
                        mapbox_style="open-street-map", zoom = 0.5, radius = 5, color_continuous_scale = 'sunsetdark', range_color = [0.0,1400000.0], animation_frame = 'Tahun')
    st.plotly_chart(fig)

    st.header("Laju Persebaran Covid-19 di Indonesia Berdasarkan Tanggal")
    df_cleaned_out['Tanggal'] = pd.to_datetime(df['Tanggal'], format = '%x')
    df_cleaned_out['Tanggal'] = df['Tanggal'].apply(str)
    
    fig = px.density_mapbox(df_cleaned_out, lat="Garis Lintang (lat)", lon="Garis Bujur (lot)", z = 'Total Kasus Baru', 
                        mapbox_style="open-street-map", zoom = 3.0, radius = 5, color_continuous_scale = 'Plasma', range_color = [10,1200.0], animation_frame = 'Tanggal')
    st.plotly_chart(fig)

def total(dataframe):
    # --- Header ---
    st.header("Total Kasus Covid-19 di Indonesia")
    st.markdown("----")

    # --- Information of total Several Data ---
    total_case, total_recovered, total_death = st.columns(3)

    total_case.metric("Total Kasus Baru", df_cleaned_out['Kasus Baru'].sum())
    total_recovered.metric("Total Sembuh",  df_cleaned_out['Sembuh'].sum())
    total_death.metric("Total Kematian",  df_cleaned_out['Kematian'].sum())

    st.markdown("----")

    # ///////

    temp = df_cleaned_out[['Tanggal', 'Kasus Baru', 'Kematian', 'Sembuh']]
    temp = temp.melt(id_vars='Tanggal', value_vars=['Kasus Baru', 'Kematian', 'Sembuh'])
    fig = px.treemap(temp, path=["variable"], values="value", height=250,
                 color_discrete_sequence=[dth, rec, cnf])
    fig.data[0].textinfo = 'label+text+value'
    # fig.update_layout(title_text='Rekap COVID 19 Indonesia 2020-2022', title_x=0.5)
    st.plotly_chart(fig)

    # bar chart
    st.write("Total Kasus Berdasarkan Provinsi")
    jenis = st.sidebar.radio("Pilih Kasus ", ('Tampilkan Semua','Terkonfirmasi','Sembuh','Meninggal'))
    nums = st.sidebar.slider('Pilih jumlah provinsi', 5,35,5)
    def plot_province(jenis, n_province):
        top_cases = df_cleaned_out.groupby('Wilayah')['Kasus Baru'].sum().reset_index().sort_values(by='Kasus Baru', ascending=False).head(n_province)
        top_death = df_cleaned_out.groupby('Wilayah')['Kematian'].sum().reset_index().sort_values(by='Kematian', ascending=False).head(n_province)
        top_recovered = df_cleaned_out.groupby('Wilayah')['Sembuh'].sum().reset_index().sort_values(by='Sembuh', ascending=False).head(n_province)
        confirmed = go.Bar(
                            y=top_cases['Kasus Baru'], 
                            x=top_cases['Wilayah'], 
                            name = 'Terkonfirmasi',
                            marker={
                                'color': top_cases['Kasus Baru'],
                                'colorscale': 'Purp'}
                        )
        recovered = go.Bar(
                    y=top_recovered['Sembuh'], 
                    x=top_recovered['Wilayah'], 
                    name='Sembuh',
                    marker={
                        'color': top_recovered['Sembuh'],
                        'colorscale': 'Blugrn'}
                )

        death =  go.Bar(
                            y=top_death['Kematian'], 
                            x=top_death['Wilayah'], 
                            name='Meninggal Dunia',
                            marker={
                                'color': top_death['Kematian'],
                                'colorscale': 'Reds'}
                    )
        if jenis == 'Tampilkan Semua' :
            data = [confirmed,recovered,death]  
            fig = go.Figure(data)
            title = 'Total Kumulatif Per-Provinsi'
        elif jenis == 'Terkonfirmasi':
            data = [confirmed]
            fig = go.Figure(data)
            title = 'Total Terkonfirmasi Per-Provinsi'
        elif jenis == 'Sembuh':
            data = [recovered]
            fig = go.Figure(data)
            title = 'Total Sembuh per-Provinsi'
        else:
            data = [death]
            fig = go.Figure(data)
            title = 'Total Meninggal Per-Provinsi'
        
        fig.layout.update(
        title=title, 
        xaxis_title='Time Periode', 
        yaxis_title='Count', 
        hovermode="x"
        )
        st.plotly_chart(fig, use_container_width=True)
    plot_province(jenis, nums)

if options == 'Data Header':
    data_header(df)
elif options == 'Data Statistics':
    stats(df)
elif options == 'Tren':
    plot(df)
elif options == 'Peta Persebaran':
    mapping(df)
elif options == 'Total Kasus':
    total(df)
