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

import nltk

#--------------------CONFIGURACIÓN DE LA PÁGINA----------------------------#
st.set_page_config(page_title="Hawaii", layout="wide", page_icon="🌴")
st.set_option('deprecation.showPyplotGlobalUse', False)

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col2:
        st.image('img/welcome.jpg')

st.caption('Pedro Llamas López')
badge(type="github", name="pedrollamas")

col1, col2 = st.columns(2)
with col2:
   
   st.image("img/equipaje.jpg")
   st.text("Fuente: www.pixabay.com")
with col1:
        st.header('Introducción')
        st.markdown("<h5 style='text-align: justify;'>Hawaii es un archipiélago situado en medio del Océano Pacífico que conforma uno de los estados insulares de los Estados Unidos. Con una población total de 1.211.537 habitantes, este conjunto de islas representa uno de los destinos turísticos más importantes de la Polinesia. Su capital es Honoloulu, que es, a su vez, la ciudad más grande y poblada de toda la isla (ubicada en la isla de Oahu). A su vez, Hawaii es el nombre que recibe la isla más grande de este archipiélago; seguida en orden de importancia, por Niihau, Lanai, Maui, Kahoolawe, Molokai y Oahu. Hemos dedicado una sección sobre las islas de Hawaii, dónde encontrarás más información sobre cada isla. Este archipiélago comparte algunos parecidos con muchas de las islas perdidas en medio del océano: la composición de su suelo. Son islas volcánicas que poseen condiciones ambientales únicas en el mundo y, debido a ello, también cuentan con una fauna y flora endémica, que vale la pena conocer.</h5>", unsafe_allow_html=True)
       
col1, col2 = st.columns(2)
with col1:
        st.header('Un poco de historia de Hawaii')
        st.image('img/history.jp.jpeg')
        st.text("Fuente: www.so-rummet.se/aret-runt/james-cook-dodas-av-urinvanare-pa-hawaii")
        
with col2:

        st.markdown("<h5 style='text-align: justify;'>Los primeros habitantes de estas islas fueron colonizadores polinesios que llegaron a la isla mediante catamaranes aunque no se tienen registros de la fecha exacta de dicha conquista. Pasaría un largo tiempo hasta que llegaran los españoles, quienes lo hicieron a mediados de 1550. No obstante, no se tienen registros de una conquista, tan sólo fue un viaje que les sirvió a los peninsulares a conocer la ubicación y registrarla en sus mapas. Pasarían dos siglos hasta que se demostrara la existencia de los colonizadores españoles en la isla. No obstante, a la corona española no parecía interesarle este archipiélago.En 1810 las islas de Hawaii estaban gobernadas por Kamehameha I, en un gobierno que estaba bajo la protección británica. De hecho, su propia bandera se parecía a la del Reino Unido. Podría decirse que esta fue una de las pocas conquistas pacíficas que se le pueden adjudicar a la corona británica; tal es así que en 1820, durante el mandato de Kamehameha II, se les permitió la entrada a los misioneros y todos los dirigentes dejaron su propia religión para aceptar la nueva religión que venía de Inglaterra. De este modo, en pocos años el cristianismo protestante se expandió por toda la isla y se perdió la antigua religión de los nativos.En 1839 se creó la Primera Constitución de Hawaii. Este fue un gran paso para la vida política de la isla ya que pasó de regirse por una monarquía absoluta a fundar una monarquía constitucional. Esto sucedió durante el reinado de Kamehameha III. Años más tarde, en 1874, Hawaii firmó un tratado con Estados Unidos que permitía el derecho de comercio en concesión exclusiva con Estado Unidos. Esto potenció considerablemente la industria de la isla: hubo un impresionante crecimiento en su agricultura lo que derivó en un aumento de ofertas de trabajo que trajo consigo la llegada de una ola migratoria proveniente de Asia que cambiaría considerablemente la idiosincrasia de la isla.En 1893, después de numerosos conflictos políticos entre Estados Unidos y Hawaii, se suprimió la monarquía y el archipiélago se convirtió en un nuevo estado de Estados Unidos. Al día de hoy, su organización política se encuentra regida por las normas americanas.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col2:
        
        st.image('img/hula.jpg')
        st.text("Fuente: www.happyhawaii.es")
with col1:
        st.header('Cultura en Hawaii')
        st.markdown("<h5 style='text-align: justify;'>La diversa cultura de Hawái se expresa, entre otras cosas, en el idioma, la música, el arte, el teatro, la danza, el cine, la gastronomía y una gran cantidad de festivales. El espíritu de aloha se encuentra en el núcleo de todo: en el arco fluido de las manos de una bailarina de hula o en el ritmo suave de una guitarra slack-key. El espíritu aloha es la coordinación de mente y corazón en cada persona. Lleva a cada persona a su propio ser. Cada persona debe pensar y transmitir buenos sentimientos a los demás. En la contemplación y presencia de la fuerza vital.La isla de Hawaii ha estado habitada por distintos grupos étnicos, esto ha derivado en la formación de una cultura ecléctica, que se ha ido afirmando a lo largo del tiempo beneficiándose con la mezcla de las distintas culturas. Esto vuelve a Hawaii un destino realmente interesante ya que cuenta con un variado y auténtico bagaje artístico, destacándose las danzas, las artesanías y la gastronomía.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

# Mapa de lugares interesantes
st.title('Los imprescindibles de Hawaii')
st.markdown("<h5 style='text-align: justify;'>En el mapa se pueden ver una serie de lugares considerados imprescindibles a visitar en el archipiélago de Hawaii, playas, volcanes, parques naturales, etc.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
lugares = pd.read_csv('data/lugares.csv')
mapa_lugares = folium.Map(location=[20.592494436163758, -157.54544732848058], zoom_start=7.4, tiles="OpenStreetMap")

for lat, lon, nombre, tipo in zip(lugares['Latitud'],lugares['Longitud'],lugares['Nombre'],lugares['Tipo']):
  marker_color = 'green'
  
 
  folium.Marker(
    [lat, lon], popup=f"<b>Nombre: {nombre} <br>Tipo: {tipo}</b>",
    icon=folium.Icon(color=marker_color, icon = 'star')
).add_to(mapa_lugares)
st_folium(mapa_lugares, width= 1000, height=500, returned_objects=[])

st.title('Las palabras de la gente')
st.markdown("<h5 style='text-align: justify;'>Usando la librería nltk he sacado un mapa de palabras donde podemos ver las más repetidas por la gente.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
# Mapa de palabras
st.image("img/mapa_palabras.png")
