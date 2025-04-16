import streamlit as st
from utils.api import get_all_restaurants, get_top_rated_restaurants

def render():
    st.title("🍕 Panel Principal - Pizzabella")
    st.success(f"Bienvenido {st.session_state.user['name']} 👋")

    st.markdown("---")
    st.subheader("¿Qué deseas hacer?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔎 Ver todos los restaurantes"):
            restaurants = get_all_restaurants()
            st.session_state.restaurants = restaurants
            st.session_state.view = "all"

    with col2:
        if st.button("⭐ Ver mejores calificados"):
            top_restaurants = get_top_rated_restaurants()
            st.session_state.restaurants = top_restaurants
            st.session_state.view = "top"

    if "restaurants" in st.session_state:
        st.markdown("---")
        view_label = "Todos los restaurantes" if st.session_state.view == "all" else "Mejores calificados"
        st.subheader(view_label)
        for r in st.session_state.restaurants:
            st.markdown(f"**{r['name']}** - ⭐ {r.get('averageRating', 'N/A')}")