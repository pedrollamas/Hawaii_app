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

st.set_page_config(page_title="Turismo", layout="wide", page_icon="🏖️")

badge(type="github", name="pedrollamas")

#Defino el dataframe
listings = pd.read_csv('data/listings_procesado.csv')

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown("# Consejos para el turismo")
st.subheader('Precios por isla')

tab1, tab2, tab3, tab4 = st.tabs(["Isla de Maui, Moloka'i, Lanai", "Isla de Kauai", "Isla de O'ahu", "Isla de Hawaii"])

with tab1:
    col1, col2 = st.columns(2)
    with col2:
        feq = listings[listings['accommodates']==2]
        feq = listings[listings['neighbourhood_group'] == 'Maui']
        feq = feq.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)
        barras_maui = feq.plot.barh(figsize=(10, 8), color=['#ffff82', '#f5f7dc', '#b5d99c', '#0f0326', '#e65f5c', '#758ecd', '#328FA0', '#C0DBB2'],edgecolor = 'black', width=1)
        plt.title("Precio medio diario para una pareja en Maui", fontsize=20)
        plt.xlabel('Precio medio (€)', fontsize=12)
        plt.ylabel("")
        st.pyplot(barras_maui.figure)
        
        st.markdown("<h5 style='text-align: justify;'> Lahaina, en la isla de Maui por el contrario representa la historia de Hawaii y es conocido por ser el centro cultural del archipiélago. Con un templo budista que data de 1931, hablamos de un pueblo muy rico en historia que se ha reconvertido a un punto clave del turismo del archipélago. Siendo capital del archipiélago al principio del siglo XIX y reconocido por sus avistamientos de ballenas. Residió durante un periodo de tiempo Herman Melville, autor de Moby-Dick entre otras novelas.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
        st.image("img/lahaina.jpg")
        st.text("Lahaina")
        st.text("Fuente: www./a.cdn-hotels.com")
    
    with col1:
        feq = listings[listings['accommodates']==2] 
        feq = feq.groupby('neighbourhood')['price'].mean().sort_values(ascending=True) 
        adam = gpd.read_file("data/neighbourhoods.geojson") 
        feq = pd.DataFrame([feq]) 
        feq = feq.transpose() 

        adam = pd.merge(adam, feq, on='neighbourhood', how='left') 
        adam.rename(columns={'price': 'average_price'}, inplace=True) 
        adam.average_price = adam.average_price.round(decimals=0) 
        adam = adam.dropna(subset=['average_price']) 

        map_dict = adam.set_index('neighbourhood')['average_price'].to_dict() 
        color_scale = LinearColormap(['yellow','red','purple'], vmin=min(map_dict.values()), vmax=max(map_dict.values()), caption='Average price') 
        def get_color(feature): 
            value = map_dict.get(feature['properties']['neighbourhood']) 
            if value is None: 
                return '#BADADA' 
            else: 
                return color_scale(value) 
            
        map3 = folium.Map(location=[20.703249920196154, -156.50835426041527], zoom_start=8.5) 
        folium.GeoJson(data=adam, 
                    name='Hawaii', 
                    tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood', 'average_price'],
                                                            labels=True, 
                                                            sticky=False), 
                    style_function= lambda feature: {
                        'fillColor': get_color(feature),
                        'color': 'black',
                        'weight': 1, 
                        'dashArray': '5, 5', 
                        'fillOpacity':0.9 }, 
                    highlight_function=lambda feature: {'weight':3, 'fillColor': get_color(feature), 'fillOpacity': 0.8}).add_to(map3) 
        map3.add_child(color_scale)
        st_folium(map3, width= 1000, height=500, returned_objects=[])
        
        st.markdown("<h5 style='text-align: justify;'> Moloka'i es la isla que más se intenta resistir al turismo masificado e invasivo de todo el archipiélago hawaiano, por ello la oferta hotelera es muy reducida y alejada de lo que el típico turista espera encontrar en una isla paradisiaca. Los residentes de esta isla prefieren que el visitante venga con la intención de empaparse la cultura que ellos intentan preservar, por lo que si buscas la típica experiencia turística este no es tu lugar.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
        st.image("img/molokai.jpg")
        st.text("Molokai")
        st.text("Fuente: www.forbes.com")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        feq = listings[listings['accommodates']==2] 
        feq = feq.groupby('neighbourhood')['price'].mean().sort_values(ascending=True) 
        adam = gpd.read_file("data/neighbourhoods.geojson") 
        feq = pd.DataFrame([feq]) 
        feq = feq.transpose() 

        adam = pd.merge(adam, feq, on='neighbourhood', how='left') 
        adam.rename(columns={'price': 'average_price'}, inplace=True) 
        adam.average_price = adam.average_price.round(decimals=0) 
        adam = adam.dropna(subset=['average_price']) 

        map_dict = adam.set_index('neighbourhood')['average_price'].to_dict() 
        color_scale = LinearColormap(['yellow','red','purple'], vmin=min(map_dict.values()), vmax=max(map_dict.values()), caption='Average price') 
        def get_color(feature): 
            value = map_dict.get(feature['properties']['neighbourhood']) 
            if value is None: 
                return '#BADADA' 
            else: 
                return color_scale(value) 
        
        map3 = folium.Map(location=[22.07250350682253, -159.51822571584464], zoom_start=10.3) 
        folium.GeoJson(data=adam, 
                    name='Hawaii', 
                    tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood', 'average_price'],
                                                            labels=True, 
                                                            sticky=False), 
                    style_function= lambda feature: {
                        'fillColor': get_color(feature),
                        'color': 'black',
                        'weight': 1, 
                        'dashArray': '5, 5', 
                        'fillOpacity':0.9 }, 
                    highlight_function=lambda feature: {'weight':3, 'fillColor': get_color(feature), 'fillOpacity': 0.8}).add_to(map3) 
        map3.add_child(color_scale)
        st_folium(map3, width= 1000, height=500, returned_objects=[])
        
        st.markdown("<h5 style='text-align: justify;'>La isla de Kauai se reconoce por tener un amplio abanico de actividades, lo que la hace una isla atractiva para diferentes tipos de turistas. Desde playas de aguas cristalina, tanto accesibles como ocultas tras kms de camino a pie. Ofrece diferentes rutas de senderismo que para aquel que desea disfrutar de un día de deporte en un paraiso es perfecta. A su vez, es conocida por tener varios campos de golf, incluyendo el Princeville resort que podemos ver debajo y por último, es un lugar donde se ofrecen varias actividades acuáticas como kayak, submarinismo, etc.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
        st.image("img/princeville.jpg")
        st.text("Princeville Resort")
        
    with col2:
        st.image("img/barras_kauai.png")
        st.markdown("<h5 style='text-align: justify;'>La zona de Koloa y Poipu, que podemos observar como las más caras. Se encuentra situada en una ubicación excepcional, a escasos 15 minutos en coche del aeropuerto y 10 del campo de golf Kukuiolono. Además en sus cercanías encontramos 4 playas significativas, una escuela de vuelo y dos reservas naturales. Una ubicación ideal que tiene su efecto en el precio por noche.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
        st.image("img/koloa.jpg")
        st.text("Koloa Landing Resort")

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        feq = listings[listings['accommodates']==2] 
        feq = feq.groupby('neighbourhood')['price'].mean().sort_values(ascending=True) 
        adam = gpd.read_file("data/neighbourhoods.geojson") 
        feq = pd.DataFrame([feq]) 
        feq = feq.transpose() 

        adam = pd.merge(adam, feq, on='neighbourhood', how='left') 
        adam.rename(columns={'price': 'average_price'}, inplace=True) 
        adam.average_price = adam.average_price.round(decimals=0) 
        adam = adam.dropna(subset=['average_price']) 

        map_dict = adam.set_index('neighbourhood')['average_price'].to_dict() 
        color_scale = LinearColormap(['yellow','red','purple'], vmin=min(map_dict.values()), vmax=max(map_dict.values()), caption='Average price') 
        def get_color(feature): 
            value = map_dict.get(feature['properties']['neighbourhood']) 
            if value is None: 
                return '#BADADA' 
            else: 
                return color_scale(value) 
            
        map3 = folium.Map(location=[21.47390943260042, -157.99133209364058], zoom_start=10) 
        folium.GeoJson(data=adam, 
                    name='Hawaii', 
                    tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood', 'average_price'],
                                                            labels=True, 
                                                            sticky=False), 
                    style_function= lambda feature: {
                        'fillColor': get_color(feature),
                        'color': 'black',
                        'weight': 1, 
                        'dashArray': '5, 5', 
                        'fillOpacity':0.9 }, 
                    highlight_function=lambda feature: {'weight':3, 'fillColor': get_color(feature), 'fillOpacity': 0.8}).add_to(map3) 
        map3.add_child(color_scale)
        st_folium(map3, width= 1000, height=500, returned_objects=[])
        
        st.markdown("<h5 style='text-align: justify;'>Es la isla más poblada y conocida del archipiélago, con alrededor de 900.000 habitantes, en la que se encuentra la capital Honolulú. Alberga diferentes atractivos turísticos como la base naval de Pearl Harbor, la propia ciudad de Honolulú, la bahía de Hanauma, ideal para hacer buceo y la Diamond Head, una toba volcánica que goza de un importante prestigio.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
        st.image("img/harbor.jpg")
        st.text("Pearl Harbor memorial")
        
    with col2:
        st.image("img/barras_honolulu.png")
        st.image("img/diamond.jpg")
        st.text("Diamond Head")
        
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        feq = listings[listings['accommodates']==2] 
        feq = feq.groupby('neighbourhood')['price'].mean().sort_values(ascending=True) 
        adam = gpd.read_file("data/neighbourhoods.geojson") 
        feq = pd.DataFrame([feq]) 
        feq = feq.transpose() 

        adam = pd.merge(adam, feq, on='neighbourhood', how='left') 
        adam.rename(columns={'price': 'average_price'}, inplace=True) 
        adam.average_price = adam.average_price.round(decimals=0) 
        adam = adam.dropna(subset=['average_price']) 

        map_dict = adam.set_index('neighbourhood')['average_price'].to_dict() 
        color_scale = LinearColormap(['yellow','red','purple'], vmin=min(map_dict.values()), vmax=max(map_dict.values()), caption='Average price') 
        def get_color(feature): 
            value = map_dict.get(feature['properties']['neighbourhood']) 
            if value is None: 
                return '#BADADA' 
            else: 
                return color_scale(value) 
            
        map3 = folium.Map(location=[19.618612200526616, -155.52568556129822], zoom_start=9) 
        folium.GeoJson(data=adam, 
                    name='Hawaii', 
                    tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood', 'average_price'],
                                                            labels=True, 
                                                            sticky=False), 
                    style_function= lambda feature: {
                        'fillColor': get_color(feature),
                        'color': 'black',
                        'weight': 1, 
                        'dashArray': '5, 5', 
                        'fillOpacity':0.9 }, 
                    highlight_function=lambda feature: {'weight':3, 'fillColor': get_color(feature), 'fillOpacity': 0.8}).add_to(map3) 
        map3.add_child(color_scale)
        st_folium(map3, width= 1000, height=500, returned_objects=[])
        
        st.markdown("<h5 style='text-align: justify;'>Hilo es la ciudad más grande de la isla de Hawaii con alrededor de 50.000 habitantes. Por ello los alojamientos son más baratos que como podemos observar en Kohala, que se encuentra entre dos reservas naturales y tiene alojamientos en poblaciones más exclusivas. En south Kohala se encuentran una serie de resorts cercanos a un club de golf que encarecen la estancia promedio.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
        st.image("img/hilo.jpg")
    
    with col2:
        st.image("img/barras_hawaii.png")
        st.image("img/mauna.jpg")
        
    
        
