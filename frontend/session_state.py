import streamlit as st

def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "restaurants" not in st.session_state:
        st.session_state.restaurants = []
    if "view" not in st.session_state:
        st.session_state.view = None
