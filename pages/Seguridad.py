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

st.set_page_config(page_title="Seguridad", layout="wide", page_icon="🌪️")

#Defino el dataframe
listings = pd.read_csv('data/listings_procesado.csv')

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

badge(type="github", name="pedrollamas")

#Defino el dataframe
huracanes = pd.read_csv('data/refugios.csv')

st.markdown("# Análisis de la seguridad en Hawaii")
st.text("opendata.hawaii.gov")

st.markdown("<h5 style='text-align: justify;'>Debido al cambio de las condiciones climáticas en todo nuestro planeta, me pregunté si existía la posibilidad de presenciar un huracán o catástrofe similar durante nuestra estancia en Hawaii. Sin embargo, los huracanes rara vez tocan tierra en las islas hawaianas, pero los ciclones tropicales en el océano pacífico ocasionalmente generan algún problema. Por ello y de cara a asegurar la seguridad del ciudadano hawaiiano y del turista consulté la página estatal donde nos proporcionan una serie de refugios, con diferentes características donde podemos alojarnos en caso de alguna emergencia ya sea climática o de otra índole.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

# Insertamos un checkbox para mostrar o no el Dataframe
if st.checkbox('Mostrar Dataframe'):
    huracanes

st.markdown("<h5 style='text-align: justify;'>Después de realizar el correspondiente preprocesamiento de los datos y extraer las latitudes y longitudes del documento, he realizado un mapa con las localizaciones y características que nos pueden ser de utilidad.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

    # Creamos el mapa
m = folium.Map(location=[20.674868371975755, -157.529547511304], zoom_start=7.4, tiles="Stamen Terrain")

for lat, lon, shelter, special_needs, pet_friendly in zip(huracanes['latitud'],huracanes['longitud'],huracanes['Hurricane Shelter'],huracanes['Special Needs'],huracanes['Pet Friendly']):
  marker_color = 'purple'
  folium.Marker(
    [lat, lon], popup=f"<b>Hurricane Shelter: {shelter} <br> Special Needs: {special_needs} <br> Pet Friendly: {pet_friendly} </b>",
    icon=folium.Icon(color=marker_color, icon = 'flag')
).add_to(m)
st_folium(m, width= 1000, height=500, returned_objects=[])