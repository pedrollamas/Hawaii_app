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

st.set_page_config(page_title="Legal", layout="wide", page_icon="👨‍⚖️")

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """

listings = pd.read_csv('data/listings_procesado.csv')

st.markdown(hide_menu_style, unsafe_allow_html=True)

badge(type="github", name="pedrollamas")

st.markdown("# Análisis legal")

col1, col2 = st.columns(2)
with col1:
    st.subheader('Definición de Hawaii sobre alquileres a corto plazo')
    st.markdown("<h5 style='text-align: justify;'> El estado de Hawaii no tiene una definición unificada respecto a los alquileres a corto plazo. La mayoría de ciudades lo definen como aquellos alojamientos que se alquilan por menos de 30 días consecutivos, a cambio de una remuneración. Otros lugares, como Honolulu, expanden ese criterio para incluir anuncios cuya duración llegue hasta 90 días.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

with col2:
    st.subheader('Novedades alquileres a corto plazo en Honolulu')
    st.markdown("<h5 style='text-align: justify;'> Los Bed & Breakfast que están siendo actualmente alquilados en periodos de 30 - 89 días serán considerados a partir del 23 de Abril de 2023 como alojamientos a largo plazo. Por lo tanto, pasarán a tener otra consideración legal.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Deducción fiscal en Hawaii')
    st.markdown("<h5 style='text-align: justify;'> De acuerdo a la normativa federal, los propietarios de Airbnbs en Hawaii tienen acceso a tener deducciones fiscales si alquilan una vivienda al menos 14 días al año. El estado de Hawaii lleva a cabo esta deducción con el objetivo de facilitar una mayor oferta de alojamientos vacacionales y favorecer a los inversores recuperar su inversión.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

with col2:
    st.subheader('Alquileres a corto plazo en Kauai')
    st.markdown("<h5 style='text-align: justify;'> El condado de Kauai es otra zona del estado de Hawaii que ha establecido regulaciones restrictivas respecto a Airbnb.Los B & B, no tienen permitido ser alquilados por más de 29 días seguidos y el dueño del mismo se tiene que encontrar presente en la isla durante su alquiler.<h5 style='text-align: justify;'>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Deduccciones", "Futuras viviendas largo plazo", "Normativa 90 días", "B & B Kauai"])
with tab1:
    st.markdown("<h5 style='text-align: justify;'> Como hemos visto anteriormente, en Hawaii se proporciona una deducción para aquellas viviendas que se alquilen por 14 días al año, de ahí en parte la gran oferta que hay en Hawaii.Podemos comprobar si hay personas que quieren únicamen beneficiarse de dicha deducción estableciendo un mínimo de noches de 14 exactamente.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    listings[(listings['neighbourhood_group'] == 'Hawaii') & (listings['minimum_nights'] == 14)]
    st.markdown("<h5 style='text-align: justify;'> Como podemos observar tenemos un total de 23 anuncios con exactamente 14 días de mínima estancia en su alojamiento, por lo que podemos deducir que son personas que quieren asegurarse la deducción de impuestos que proporciona Hawaii county.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    
with tab2:
    st.markdown("<h5 style='text-align: justify;'> A partir del 23 de Abril de este año, en Hawaii, aquellas viviendas que se alquiler por más de 30 días y menos de 89 pasarán a tener la consideración de 'long-term', por lo tanto vamos a ver cuáles cumplen esa condición ya que sería interesante avisarles o bien por parte del Estado o de Airbnb para evitar que incumplan la normativa dentro de poco.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    listings[(listings['neighbourhood_group'] == 'Hawaii') & (listings['maximum_nights'] < 89) & (listings['maximum_nights'] > 30) & (listings['minimum_nights'] > 29)]
    st.markdown("<h5 style='text-align: justify;'>Podemos observar que existen un total de 8 anuncios que cuentan con las condiciones que la nueva normativa de Hawaii establecerá como alojamientos de largo plazo. Sería interesante por parte de Airbnb notificar a estos alojamientos del cambio de normativa para evitar que a partir del 23 de Abril incumplan con la nueva normativa.Como presunto cliente nuestro, deberíamos asesorar a Airbnb de ponerse en contacto con los mismos y estudiar su situación, pueden ser personas conscientes de la normativa haciendo un mal uso de la aplicación o personas que desconocen el cambio de normativa.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    
with tab3:
    st.markdown("<h5 style='text-align: justify;'> Como sabemos aquellas viviendas que estén alquiladas por más de 90 días deberían estar inscritas como viviendas de alquiler a largo plazo. Debemos estudiar si contamos con viviendas que estén haciendo un mal uso de la aplicación estableciendo un mínimo de noches de 89 o 90 días, ya que puede haebr gente que establezca 89 como límite para evitar la detección automática del sistema.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    listings[listings['minimum_nights'] > 88]
    st.markdown("<h5 style='text-align: justify;'> Como podemos ver, encontramos un total de 596 viviendas anunciadas en Airbnb que están utilizando la aplicación para realizar alquileres a largo plazo.Nuestra obligación es asesorar a Airbnb que se ponga en contacto con las autoridades para que comprueben si esas relaciones contractuales son fraudulentas.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    
with tab4:
    st.markdown("<h5 style='text-align: justify;'> Como hemos visto, los Bed and Breakfast en Kauai tienen como norma proporcionar estancias de máximo 29 días a los huéspedes. Por lo que queremos comprobar si existen anuncios en Airbnb que se anuncien como B & B pero proporcionen estancias superiores a 29 días.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
    listings[(listings['neighbourhood_group'] == 'Kauai') & (listings['minimum_nights'] > 29) & (listings['property_type'] == 'Private room in bed and breakfast')]
    st.markdown("<h5 style='text-align: justify;'> Hemos encontrado tan sólo 3 anuncios corresponientes al mismo anunciante que incumplen con la normativa en lo que respecta a Bed & Breakfast. El anunciante tiene establecido el mismo límite de 180 noches para alquilar cualquier de sus tres habitaciones privadas con la consideración de 'habitación privada en un Bed and Breakfast'.Por lo tanto, deberíamos aconsejar a Airbnb que se ponga en contacto con el anunciante o las autoridades correspondientes puesto que no se permite alquilar por encima de 29 días un B & B.<h5 style='text-align: justify;'>", unsafe_allow_html=True)