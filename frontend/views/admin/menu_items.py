import streamlit as st
from utils.api import get_all_menu_items, get_all_restaurants, create_menu_item, get_menu_image

def render():
    st.title("🧾 Gestión de platillos")

    st.markdown("### Selecciona una acción")
    opcion = st.radio(
        "Opciones disponibles:",
        (
            "📋 Ver todos los platillos",
            "➕ Crear platillo",
            "🗑️ Eliminar platillo",
            "✏️ Actualizar platillo"
        )
    )

    st.markdown("---")

    # Ver platillos
    if opcion == "📋 Ver todos los platillos":
        st.subheader("Listado completo de platillos")

        platillos = get_all_menu_items()
        if not platillos:
            st.info("No hay platillos disponibles.")
        else:
            st.success(f"Se encontraron {len(platillos)} platillos.")
            for p in platillos:
                with st.expander(p["name"]):
                    st.markdown(f"📝 **Descripción:** {p.get('description', 'Sin descripción')}")
                    st.markdown(f"💰 **Precio:** Q{p.get('price', 'No especificado')}")
                    
                    """
                    st.image(image_url)

                    """
                    image_file_id = p.get("image_file_id")
                    if image_file_id:
                        image_url = get_menu_image(p.get("image_file_id"))
                        st.image(image_url)
                    else:
                        st.write("Imagen del platillo no disponible por el momento")

                    st.caption(f"🕒 Creado: {p.get('createdAt')}")
                    st.caption(f"🔄 Actualizado: {p.get('updatedAt')}")
                
    elif opcion == "➕ Crear platillo":
        st.subheader("Crear un nuevo platillo")

        restaurants = get_all_restaurants()
        if not restaurants:
            st.error("No se pudieron cargar los restaurantes.")
            return

        restaurant_options = {r["name"]: r["_id"] for r in restaurants}

        with st.form("form_crear_platillo"):
            selected_restaurant = st.selectbox("Selecciona un restaurante", list(restaurant_options.keys()))
            restaurant_id = restaurant_options[selected_restaurant]

            name = st.text_input("Nombre del platillo")
            description = st.text_area("Descripción")
            price = st.number_input("Precio", min_value=0.0, step=0.5)
            image_file = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

            submitted = st.form_submit_button("Crear")

            if submitted:
                if not all([restaurant_id, name, description, price, image_file]):
                    st.warning("Completa todos los campos e incluye una imagen.")
                else:
                    result = create_menu_item({
                        "restaurantId": restaurant_id,
                        "name": name,
                        "description": description,
                        "price": price,
                    }, image_file)

                    if result:
                        st.success(f"Platillo '{name}' creado correctamente.")
                    else:
                        st.error("Error al crear el platillo.")
