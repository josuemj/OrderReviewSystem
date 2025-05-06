import streamlit as st
from utils.api import get_all_menu_items, get_all_restaurants, create_menu_item, get_menu_image, delete_menu_item, update_menu_item, create_menu_items_bulk
import time
def render():
    st.title("🧾 Gestión de platillos")

    st.markdown("### Selecciona una acción")
    opcion = st.radio(
        "Opciones disponibles:",
        (
            "📋 Ver todos los platillos",
            "➕ Crear platillo",
            "🤌 Crear varios platillos",
            "✏️ Actualizar platillo"
        )
    )

    st.markdown("---")

    # Ver platillos
    if opcion == "📋 Ver todos los platillos":
        st.subheader("Listado completo de platillos")
        st.write("Tambien puedes elimar al desplegar")

        platillos = get_all_menu_items()
        if not platillos:
            st.info("No hay platillos disponibles.")
        else:
            st.success(f"Se encontraron {len(platillos)} platillos.")
            for p in platillos:
                with st.expander(p["name"]):  # solo un expander
                    st.markdown(f"📝 **Descripción:** {p.get('description', 'Sin descripción')}")
                    st.markdown(f"💰 **Precio:** Q{p.get('price', 'No especificado')}")

                    image_file_id = p.get("image_file_id")
                    if image_file_id:
                        image_url = get_menu_image(image_file_id)
                        st.image(image_url)
                    else:
                        st.write("📷 Imagen del platillo no disponible")

                    st.caption(f"🕒 Creado: {p.get('createdAt')}")
                    st.caption(f"🔄 Actualizado: {p.get('updatedAt')}")

                    # 🔴 Botón de eliminar
                    if st.button(f"🗑️ Eliminar '{p['name']}'", key="del_" + p["_id"]):
                        if delete_menu_item(p["_id"]):
                            st.success("Platillo eliminado correctamente.")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("No se pudo eliminar el platillo.")

                    # ✏️ Formulario para actualizar
                    st.write("✏️ actualizar el platillo")
                    with st.form(f"form_actualizar_{p['_id']}"):
                        new_name = st.text_input("Nuevo nombre", value=p["name"])
                        new_description = st.text_area("Nueva descripción", value=p["description"])
                        new_price = st.number_input("Nuevo precio", value=float(p["price"]))
                        new_image = st.file_uploader("Nueva imagen (opcional)", type=["jpg", "jpeg", "png"])

                        submitted = st.form_submit_button("Actualizar")
                        if submitted:
                            update_data = {
                                "restaurantId": p["restaurantId"],
                                "name": new_name,
                                "description": new_description,
                                "price": new_price
                            }
                            success = update_menu_item(p["_id"], update_data, new_image)
                            if success:
                                st.success("Platillo actualizado correctamente")
                                st.rerun()
                            else:
                                st.error("Error al actualizar el platillo")

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
                        
    elif opcion == "🤌 Crear varios platillos":
        
        st.subheader("Crear varios platillos de forma masiva")

        restaurants = get_all_restaurants()
        if not restaurants:
            st.error("No se pudieron cargar los restaurantes.")
            st.stop()

        restaurant_options = {r["name"]: r["_id"] for r in restaurants}
        selected_restaurant = st.selectbox("Selecciona un restaurante", list(restaurant_options.keys()))
        restaurant_id = restaurant_options[selected_restaurant]

        if "bulk_menu_items" not in st.session_state:
            st.session_state.bulk_menu_items = []

        st.markdown("### ➕ Añadir platillo a la lista")
        with st.form("form_agregar_bulk"):
            name = st.text_input("Nombre del platillo")
            description = st.text_area("Descripción")
            price = st.number_input("Precio", min_value=0.0, step=0.5)
            image_file = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

            if st.form_submit_button("Agregar a la lista"):
                if not all([name, description, price, image_file]):
                    st.warning("Completa todos los campos e incluye imagen.")
                else:
                    st.session_state.bulk_menu_items.append({
                        "name": name,
                        "description": description,
                        "price": price,
                        "image": image_file
                    })
                    st.success(f"Platillo '{name}' añadido a la lista")

        # Mostrar resumen de lo agregado
        if st.session_state.bulk_menu_items:
            st.markdown("### 📝 Platillos en la lista para guardar")
            for i, item in enumerate(st.session_state.bulk_menu_items):
                st.markdown(f"**{i+1}. {item['name']}** - Q{item['price']}")
                st.caption(f"📝 {item['description']}")
                st.image(item["image"], width=200)
                if st.button(f"❌ Eliminar", key=f"delete_{i}"):
                    st.session_state.bulk_menu_items.pop(i)
                    st.rerun()

            if st.button("🚀 Crear todos los platillos"):
                result = create_menu_items_bulk(restaurant_id, st.session_state.bulk_menu_items)
                if result:
                    st.success(f"Se crearon {result['inserted_count']} platillos.")
                    st.session_state.bulk_menu_items = []
                    st.rerun()
                else:
                    st.error("Error al crear los platillos.")
        else:
            st.info("No has agregado platillos aún.")
