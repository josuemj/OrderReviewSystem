import streamlit as st
import pydeck as pdk
from utils.api import get_all_restaurants, create_new_categories_to_restaurant, remove_categories_from_restaurant, create_restaurant, update_restaurant, get_all_menu_items

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
        menu_items = get_all_menu_items()

        menu_options = {
            f"{item['name']} ({item['_id']})": item['_id']
            for item in menu_items
        }

        name = st.text_input("Nombre del restaurante")
        address = st.text_input("Dirección")
        city = st.text_input("Ciudad")

        st.markdown("### Ubicación del restaurante")

        # Estado inicial por defecto (Guatemala)
        if "new_restaurant_coords" not in st.session_state:
            st.session_state.new_restaurant_coords = {"lat": 14.6349, "lng": -90.5069}

        # Mostrar mapa con marcador actual
        view_state = pdk.ViewState(
            longitude=st.session_state.new_restaurant_coords["lng"],
            latitude=st.session_state.new_restaurant_coords["lat"],
            zoom=14
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{
                "position": [st.session_state.new_restaurant_coords["lng"], st.session_state.new_restaurant_coords["lat"]],
                "color": [255, 0, 0],
                "radius": 100
            }],
            get_position="position",
            get_color="color",
            get_radius="radius"
        )

        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v11",
            initial_view_state=view_state,
            layers=[layer]
        ))

        # Inputs de coordenadas actualizables
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitud", value=st.session_state.new_restaurant_coords["lat"], key="lat_input")
        with col2:
            lng = st.number_input("Longitud", value=st.session_state.new_restaurant_coords["lng"], key="lng_input")

        # Guardar en sesión
        st.session_state.new_restaurant_coords = {"lat": lat, "lng": lng}

        categories = st.multiselect("Categorías", ALL_CATEGORIES)

        selected_items = st.multiselect(
            "Selecciona ítems del menú para este restaurante",
            options=list(menu_options.keys())
        )
        selected_menu_ids = [menu_options[label] for label in selected_items]

        if st.button("Guardar"):
            data = {
                "name": name,
                "location": {
                    "address": address,
                    "city": city,
                    "coordinates": {
                        "lat": st.session_state.new_restaurant_coords["lat"],
                        "lng": st.session_state.new_restaurant_coords["lng"]
                    }
                },
                "categories": categories,
                "menu": selected_menu_ids
            }
            created = create_restaurant(data)
            if created:
                st.success("Restaurante creado exitosamente")
                st.rerun()
            else:
                st.error("Error al crear restaurante")


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
                st.markdown(f"📍 **Dirección:** {r['location']['address']}, {r['location']['city']}")
                st.markdown(f"🌍 **Coordenadas:** Lat {r['location']['coordinates']['lat']}, Lng {r['location']['coordinates']['lng']}")
                st.markdown(f"🏷️ **Categorías:** {', '.join(r['categories']) if r['categories'] else 'Ninguna'}")
                st.markdown(f"📋 **Ítems en el menú:** {len(r['menu'])}")
                st.markdown(f"🕒 **Creado en:** {r['createdAt']}")
                st.markdown(f"🔄 **Última actualización:** {r['updatedAt']}")

        

    elif opcion == "🔄 Actualizar datos":
        st.subheader("Actualizar datos de un restaurante")
        restaurants = get_all_restaurants()
        menu_items = get_all_menu_items()

        menu_options = {
            f"{item['name']} ({item['_id']})": item['_id']
            for item in menu_items
        }


        for re in restaurants:
                with st.expander(f"{re['name']}"):
                    edit_name = st.text_input("Nombre", value=re["name"], key=f"edit_nombre_{re['_id']}")
                    edit_address = st.text_input("Dirección", value=re['location']['address'], key=f"edit_direccion_{re['_id']}")
                    edit_city = st.text_input("Ciudad", value=re['location']['city'], key=f"edit_ciudad_{re['_id']}")

                    st.markdown("### Ubicación del restaurante")


                    # Mostrar mapa con marcador actual
                    view_state = pdk.ViewState(
                        longitude=re['location']['coordinates']['lng'],
                        latitude=re['location']['coordinates']["lat"],
                        zoom=14
                    )

                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=[{
                            "position": [re['location']['coordinates']['lng'], re['location']['coordinates']["lat"]],
                            "color": [255, 0, 0],
                            "radius": 100
                        }],
                        get_position="position",
                        get_color="color",
                        get_radius="radius"
                    )

                    st.pydeck_chart(pdk.Deck(
                        map_style="mapbox://styles/mapbox/streets-v11",
                        initial_view_state=view_state,
                        layers=[layer]
                    ))

                    # Inputs de coordenadas actualizables
                    col1, col2 = st.columns(2)
                    with col1:
                        lat = st.number_input("Latitud", value=re['location']['coordinates']["lat"], key=f"lat_input_{re['_id']}")
                    with col2:
                        lng = st.number_input("Longitud", value=re['location']['coordinates']['lng'], key=f"lng_input_{re['_id']}")
                    
                    categories = st.multiselect("Categorías", ALL_CATEGORIES, key=f"edit_categorias_{re['_id']}", default=re.get("categories", []),)

                    selected_items = st.multiselect(
                        "Selecciona ítems del menú para este restaurante",
                        options=list(menu_options.keys()),
                        default=[
                            f"{item['name']} ({item['_id']})"
                            for item in menu_items if item['_id'] in re.get("menu", [])
                        ],
                        key=f"edit_menu_{re['_id']}"
                    )
                    selected_menu_ids = [menu_options[label] for label in selected_items]
                    
                    if st.button("Actualizar", key=f"keep_key_{re['_id']}"):
                        data = {
                            "name": edit_name,
                            "location": {
                                "address": edit_address,
                                "city": edit_city,
                                "coordinates": {
                                    "lat": lat,
                                    "lng": lng
                                }
                            },
                            "categories": categories,
                            "menu": selected_menu_ids
                        }
                        updated = update_restaurant(re['_id'], data)  
                        if updated:
                            st.success("Restaurante actualizado exitosamente")
                            st.rerun()
                        else:
                            st.error("Error al actualizar restaurante")


