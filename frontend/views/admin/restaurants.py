import streamlit as st
from utils.api import get_all_restaurants, create_new_categories_to_restaurant, remove_categories_from_restaurant

ALL_CATEGORIES = [
    "Italiana", "Pizzería", "Postres", "Rápida", "Vegetariana",
    "Mexicana", "China", "Japonesa", "India", "Mediterránea",
    "Tailandesa", "Francesa", "Barbacoa", "Vegana", "Mariscos",
    "Hamburguesas", "Cafetería", "Panadería", "Comida Fusión"
]

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

        restaurants = get_all_restaurants()

        for r in restaurants:
            with st.expander(f"{r['name']}"):
                st.markdown(f"📍 Dirección: {r['location']['address']}")
                st.markdown("**Categorías actuales:**")
                st.write(", ".join(r["categories"]))

                categorias_actuales = r["categories"]
                categorias_agregar = list(set(ALL_CATEGORIES) - set(categorias_actuales))

                categorias_a_agregar = st.multiselect(
                    "Selecciona categorías para agregar",
                    options=categorias_agregar,
                    key=f"agregar_{r['_id']}"
                )

                categorias_a_eliminar = st.multiselect(
                    "Selecciona categorías para eliminar",
                    options=categorias_actuales,
                    key=f"eliminar_{r['_id']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("➕ Agregar", key=f"btn_agregar_{r['_id']}"):
                        response = create_new_categories_to_restaurant(r["_id"], categorias_a_agregar)
                        st.success("Categorías agregadas exitosamente" if response else "Error al agregar categorías")

                with col2:
                    if st.button("❌ Eliminar", key=f"btn_eliminar_{r['_id']}"):
                        response = remove_categories_from_restaurant(r["_id"], categorias_a_eliminar)
                        st.success("Categorías eliminadas exitosamente" if response else "Error al eliminar categorías")


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
