import streamlit as st
from utils.api import get_all_restaurants

def render():
    st.title("Gestor de ordenes")
    st.text("Cambiar de estado ordenes")
    st.subheader("Elegir un restaurante") # drop down