import streamlit as st
from utils.api import get_all_restaurants

def render():
    st.title("Gestionar restaurantes")
    st.text("CRUD restaurante")

    st.markdown("### Selecciona una acción")

    # Selección única tipo radio (más cómodo que muchos botones apretados)
    opcion = st.radio(
        "¿Qué deseas hacer?",
        (
            "➕ Crear restaurante",
            "✏️ Editar categorías",
            "🗑️ Eliminar restaurante",
            "📋 Ver restaurantes",
            "🔄 Actualizar datos"
        )
    )

    st.markdown("---")  # Separador visual

    if opcion == "➕ Crear restaurante":
        st.subheader("Crear un nuevo restaurante")
        st.button("Guardar")

    elif opcion == "✏️ Editar categorías":
        st.subheader("Editar categorías del restaurante")
        st.button("Actualizar")

    elif opcion == "🗑️ Eliminar restaurante":
        st.subheader("Eliminar un restaurante")
        st.button("Eliminar")

    elif opcion == "📋 Ver restaurantes":
        st.subheader("Lista de restaurantes")
        restaurants = get_all_restaurants()
        for r in restaurants:
            with st.expander(f"{r['name']}"):
                st.markdown(f"📍 Ubicación: {r["location"]["address"]}")

        

    elif opcion == "🔄 Actualizar datos":
        st.subheader("Actualizar datos de un restaurante")
        st.button("Actualizar")
