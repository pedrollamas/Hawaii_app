import streamlit as st 
from streamlit_extras.badges import badge
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="Recursos", layout="wide", page_icon="🗂️")

st.caption('Pedro Llamas López')
badge(type="github", name="pedrollamas")

rain(
    emoji="🌴",
    font_size=50,
    falling_speed=6,
    animation_length="infinite",
)

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



st.title("Páginas consultadas para la realización del proyecto")
st.markdown("<h5 style='text-align: justify;'>Folium map types and markers.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://python-visualization.github.io/folium/quickstart.html")
st.markdown("<h5 style='text-align: justify;'>Author: Dariga Kokenova. Guide of folium markers<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://darigak.medium.com/your-guide-to-folium-markers-b9324fc7d65d")
st.markdown("<h5 style='text-align: justify;'>Streamlit documentation.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://docs.streamlit.io/")
st.markdown("<h5 style='text-align: justify;'>Author: Fanilo Andrianasolo. Streamlit widgets.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://www.youtube.com/watch?v=Yd_W0sU1Fx4")
st.markdown("<h5 style='text-align: justify;'>Useful information about Hawaii.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://www.viajarhawaii.com/informacion-hawaii.php")
st.markdown("<h5 style='text-align: justify;'>Streamlit extras.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://extras.streamlit.app/Switch%20page%20function")
st.markdown("<h5 style='text-align: justify;'>Folium representation on Streamlit.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://folium.streamlit.app/dynamic_map_vs_rerender")
st.markdown("<h5 style='text-align: justify;'>Consulting chatGPT.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://openai.com/")
st.markdown("<h5 style='text-align: justify;'>Author: Avra. Tricks to make your web-application look better.<h5 style='text-align: justify;'>", unsafe_allow_html=True)
st.text("https://medium.com/@avra42/streamlit-python-cool-tricks-to-make-your-web-application-look-better-8abfc3763a5b")

