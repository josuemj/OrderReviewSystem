import streamlit as st
from utils.api import get_top_selling_menu_items
import random

def render():
    st.title("Stats")
    st.text("Stats de ventas de platillos, etc.")

    top = st.number_input("¿Cuántos platillos top quieres ver?", min_value=1, value=5, step=1)

    if top <= 0:
        st.error("El número debe ser mayor a 0.")
        return

    if st.button("Obtener Top Platillos"):
        with st.spinner('Cargando platillos más vendidos...'):
            top_items = get_top_selling_menu_items(top)

        if top_items:
            st.success("Platillos más vendidos:")
            for item in top_items:
                render_colored_title(f"🍽️ {item['menuItem_name']}")
                st.subheader(f"Restaurante: {item['restaurant_name']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(label="Platillos Vendidos", value=item['total_sale_count'])
                with col2:
                    st.metric(label="Total en Ventas (Q)", value=f"Q{item['total_sales']}")
                
                st.markdown("---")
        else:
            st.warning("No se encontraron datos.")

def render_colored_title(title_text):
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FF33A6", "#33FFF3", "#FFC733"]
    color = random.choice(colors)
    st.markdown(f"<h1 style='color: {color};'>{title_text}</h1>", unsafe_allow_html=True)
