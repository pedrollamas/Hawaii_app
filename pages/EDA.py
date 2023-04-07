#--------------------LIBRERÍAS--------------------#
import streamlit as st 
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import plotly.express as px

import os
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Mapas interactivos
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import FastMarkerCluster
import geopandas as gpd
from branca.colormap import LinearColormap

# Gráficos de plotly
import plotly.graph_objs as go
import chart_studio.plotly as py
from plotly.offline import iplot, init_notebook_mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)

# Mining de las reviews(texto)
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from wordcloud import WordCloud

# Los warnings
import warnings
warnings.filterwarnings('ignore')

from streamlit_extras.badges import badge
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="EDA", layout="wide", page_icon="📊")

badge(type="github", name="pedrollamas")

st.markdown("# Análisis exploratorio de los datos")

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
#Defino el dataframe
listings = pd.read_csv('data/listings_procesado.csv')

# Insertamos un checkbox para mostrar o no el Dataframe
if st.checkbox('Mostrar Dataframe'):
    listings = pd.read_csv('data/listings_procesado.csv')

    listings

st.title('Islas')
tab1, tab2 = st.tabs(["Anuncios publicados", "Precios"])
with tab1:
    st.markdown("<h5 style='text-align: justify;'>Anuncios publicados en Airbnb.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    lats2018 = listings['latitude'].tolist()
    lons2018 = listings['longitude'].tolist()
    locations = list(zip(lats2018, lons2018))

    map1 = folium.Map(location=[20.592494436163758, -157.54544732848058], zoom_start=7.4)
    FastMarkerCluster(data=locations).add_to(map1)
    st_folium(map1, width= 1000, height=500, returned_objects=[])
    st.markdown("<h5 style='text-align: justify;'>Podemos observar que la oferta está muy distribuida entre Maui, Honolulu y Hawaii. En el diagrama de barras debajo podemos observar la distribución de anuncios en las diferentes islas.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

    
    freq = listings['neighbourhood_group']. value_counts().sort_values(ascending=False)
    barras_islas = freq.plot.bar(figsize=(15, 3), width=1, color = ["g","b","r"])
    st.pyplot(barras_islas.figure)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribución de precios promedio por barrio en Maui")
        df1 = listings[listings.neighbourhood_group == "Maui"][["neighbourhood","price"]]
        d = df1.groupby("neighbourhood").mean()
        sns.distplot(d)
        st.line_chart(d)
        
        st.subheader("Distribución de precios promedio por barrio en Honolulu")
        df2 = listings[listings.neighbourhood_group == "Honolulu"][["neighbourhood","price"]]
        d1 = df2.groupby("neighbourhood").mean()
        sns.distplot(d1)
        plt.show();
        st.line_chart(d1)
    with col2:
        st.subheader("Distribución de precios promedio por barrio en Hawaii")
        df3 = listings[listings.neighbourhood_group == "Hawaii"][["neighbourhood","price"]]
        d2 = df3.groupby("neighbourhood").mean()
        sns.distplot(d2)
        plt.show();
        st.line_chart(d2)
        
        st.subheader("Distribución de precios promedio por barrio en Kauai")
        df4 = listings[listings.neighbourhood_group == "Kauai"][["neighbourhood","price"]]
        d3 = df4.groupby("neighbourhood").mean()
        sns.distplot(d3)
        plt.show();
        st.line_chart(d3)

st.title('Vecindarios')

feq=listings['neighbourhood'].value_counts().sort_values(ascending=True)
feq = feq [feq > 400]
feq = feq.sort_values(ascending=False)
feq.plot.barh(figsize=(10, 8), color='b', width=1)
plt.title("Anuncios clasificados por vecindario", fontsize=20)
plt.xlabel('Cantidad de anuncios', fontsize=12)
plt.show()
st.bar_chart(feq)



st.title('Tipos de propiedades y habitaciones')
tab1, tab2, tab3 = st.tabs(["Tipos de propiedades", "Tipos de habitaciones", "Número de huéspedes"])

with tab1:    
    prop = listings.groupby(['property_type','room_type']).room_type.count()
    prop = prop.unstack()
    prop['total'] = prop.iloc[:,0:3].sum(axis = 1)
    prop = prop.sort_values(by=['total'])
    prop = prop[prop['total']>=400]
    prop = prop.drop(columns=['total'])
    fig3 = px.bar(prop, orientation='h', barmode='stack',width=800, height=500)
    plt.title('Tipos de propiedades en Hawaii', fontsize=18)
    plt.xlabel('Cantidad de anunciados', fontsize=14)
    plt.ylabel("")
    plt.legend(loc = 4,prop = {"size" : 13})
    plt.rc('ytick', labelsize=13)
    plt.show()
    fig3.update_layout(title='Tipo de propiedades en el archipiélago con más de 400 alojamientos', xaxis_title='',yaxis_title='', legend_title='', font_size=14,legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='right', x=1),title_font_size=24)
    st.plotly_chart(fig3, use_container_width=True)
    
with tab2:
    freq = listings['room_type']. value_counts().sort_values(ascending=True)
    fig2 = px.bar(freq, orientation='h', barmode='stack',width=800, height=500)
    plt.show()
    st.plotly_chart(fig2, use_container_width=True)
    
    
with tab3:
    feq=listings['accommodates'].value_counts().sort_index()
    fig4 = px.bar(feq, orientation='v', barmode='stack',width=800, height=500)
    plt.title("Cantidad de huéspedes", fontsize=20)
    plt.ylabel('Cantidad de anuncios', fontsize=12)
    plt.xlabel('Huéspedes', fontsize=12)
    plt.show()
    fig4.update_layout(title='Cantidad de anuncios ofertados en función de los huéspedes que aceptan', xaxis_title='Huéspedes',yaxis_title='Anuncios', legend_title='', font_size=14,legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='right', x=1),title_font_size=24)
    st.plotly_chart(fig4, use_container_width=True)