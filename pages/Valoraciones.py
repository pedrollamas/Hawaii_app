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
import plotly.io as pio
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)
import cufflinks as cf

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

st.set_page_config(page_title="Valoraciones", layout="wide", page_icon="⭐")

badge(type="github", name="pedrollamas")

#Defino el dataframe
listings = pd.read_csv('data/listings_procesado.csv')

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown("# Reviews")
st.markdown("<h5 style='text-align: justify;'>En esta página tendremos en cuenta las diferentes puntuaciones para sacar conclusiones acerca de los alojamientos en el archipiélago de Hawaii.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Localización y Precio", "Buenos propietarios", "Disponibilidad de los alojamientos"])

with tab1:
    st.markdown("<h5 style='text-align: justify;'>En primer lugar, vamos a ver la comparativa de precio y localización por isla.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    fig = plt.figure(figsize=(20,10))
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=20)

    ax1 = fig.add_subplot(121)
    feq = listings[listings['number_of_reviews']>=10]
    feq1 = feq.groupby('neighbourhood_group')['review_scores_location'].mean().sort_values(ascending=True)
    ax1=feq1.plot.barh(color='b', width=1)
    plt.title("Puntuación media por localización", fontsize=20)
    plt.xlabel('Puntuación', fontsize=20)
    plt.ylabel("")

    ax2 = fig.add_subplot(122)
    feq = listings[listings['accommodates']==2]
    feq2 = feq.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=True)
    ax2=feq2.plot.barh(color='b', width=1)
    plt.title("Precio medio diario para dos personas", fontsize=20)
    plt.xlabel('Precio medio diario', fontsize=20)
    plt.ylabel("")

    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("<h5 style='text-align: justify;'>En segunda lugar, vamos a ver la comparativa de precio y localización por barrio.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    fig = plt.figure(figsize=(20,10))
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=20)

    ax1 = fig.add_subplot(121)
    feq = listings[listings['number_of_reviews']>=20]
    feq1 = feq.groupby('neighbourhood')['review_scores_location'].mean().sort_values(ascending=True)
    ax1=feq1.plot.barh(color='b', width=1)
    plt.title("Puntuación media por localización", fontsize=20)
    plt.xlabel('Puntuación', fontsize=20)
    plt.ylabel("")

    ax2 = fig.add_subplot(122)
    feq = listings[listings['accommodates']==2]
    feq2 = feq.groupby('neighbourhood')['price'].mean().sort_values(ascending=True)
    ax2=feq2.plot.barh(color='b', width=1)
    plt.title("Precio medio diario para dos personas", fontsize=20)
    plt.xlabel('Precio medio diario', fontsize=20)
    plt.ylabel("")

    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("<h5 style='text-align: justify;'>La que mejor puntuación obtiene es Lanai, que se encuentra al oeste de la isla de Maui, donde se encuentra Hana, la segunda zona mejor valorada.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

with tab2:
    st.image("img/superhost.png")
    listings10 = listings[listings['number_of_reviews']>=50]
    fig = plt.figure(figsize=(20,10))
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=20)

    ax3 = fig.add_subplot(121)

    ax1= plt.hist(feq1)
    plt.title("Ratio de respuesta", fontsize=20)
    plt.ylabel("número de anuncios")
    plt.xlabel("porcentaje", fontsize=20)

    ax4 = fig.add_subplot(122)
    feq2 = listings10['host_response_time'].value_counts()
    ax4=feq2.plot.bar(color='b', width=1, rot=45)
    plt.title("Tiempo de respuesta", fontsize=20)
    plt.ylabel("número de anuncios")

    plt.tight_layout()
    st.pyplot(fig)

with tab3:
    st.image("img/anuncios_fecha.png")

    st.markdown("<h5 style='text-align: justify;'>Lo que vemos es que los meses de principio de año tienen un precio medio superior y coincide con los meses que menos oferta tenemos en el cuadro superior. Por otro lado, los meses veraniegos que tienen una mayor oferta presentan precios medios más bajos.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    st.image("img/precio_por_dia.png")
    