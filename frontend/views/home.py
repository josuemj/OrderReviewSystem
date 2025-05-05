import streamlit as st
from utils.api import get_all_restaurants, get_top_rated_restaurants, get_avg_rating_by_restaurant, get_menu_items_by_restaurant, set_order, get_restaurants_by_category, get_categories
import pandas as pd

ALL_CATEGORIES = get_categories()


def render():
    st.title("🍕 Panel Principal - Pizzabella")
    st.success(f"Bienvenido {st.session_state.user["name"]} 👋")

    st.markdown("---")
    st.subheader("¿Qué deseas hacer?")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔎 Ver todos los restaurantes"):
            restaurants = get_all_restaurants()
            st.session_state.restaurants = restaurants
            st.session_state.view = "all"
        
        if st.button("Ordenar"):
            restaurants = get_all_restaurants()
            st.session_state.restaurants = restaurants
            st.session_state.view = "order"

    with col2:
        if st.button("⭐ Ver mejores calificados"):
            top_restaurants = get_top_rated_restaurants()
            st.session_state.restaurants = top_restaurants
            st.session_state.view = "top"
    
    with col3:
        if st.button("🕵️ Buscar por categorías"):
            st.session_state.view = "category_search"
            st.session_state.selected_category = ALL_CATEGORIES[0]  # Valor por defecto inicial

        if st.session_state.get("view") in ["category_search", "category_results"]:
            selected = st.selectbox(
                "Selecciona una categoría", 
                ALL_CATEGORIES, 
                index=ALL_CATEGORIES.index(st.session_state.get("selected_category", ALL_CATEGORIES[0]))
            )
            st.session_state.selected_category = selected

            if st.button("🔍 Buscar restaurantes con esa categoría"):
                filtered = get_restaurants_by_category(selected)
                st.session_state.restaurants = filtered
                st.session_state.view = "category_results"

        if st.session_state.get("view") == "category_results":
            st.subheader(f"Restaurantes en categoría: {st.session_state.selected_category}")


    st.markdown("---")
    if "restaurants" in st.session_state:
        view_map = {
            "all": "Todos los restaurantes",
            "order": "Ordenar",
            "top": "Mejores Calificados"
        }

        view_label = view_map.get(st.session_state.view, "")
        st.subheader(view_label)

        for r in st.session_state.restaurants:
            
            print(type(r))
            print(r)
            restaurant_id = r["_id"] if "_id" in r else r["id"]
            lat = r["location"]["coordinates"]["lat"]
            lon = r["location"]["coordinates"]["lng"]
            
            with st.expander(f"{r['name']}"):

                st.markdown(f"📍 Ubicación: {r["location"]["address"]}")
                st.markdown(f"🌆 City {r["location"]["city"]}")
                st.markdown(f"🏷️ Categorías: {', '.join(r.get('categories', []))}")
                
                if view_label == "Todos los restaurantes" or view_label == "Mejores Calificados":
                    details = get_avg_rating_by_restaurant(restaurant_id) or {}
                    avg = round(details.get("averageRating", 0), 2)
                    count = details.get("totalReviews", 0)
                    st.markdown(f"⭐ Promedio: `{avg}` ({count} reseñas)")
                    st.map(pd.DataFrame([{"lat": lat, "lon": lon}]))

                if view_label == "Ordenar":
                    if st.button(" 🚚 Menu 🍕", key=restaurant_id):
                        menu_items = get_menu_items_by_restaurant(restaurant_id)
                        st.session_state.menu_items = menu_items
                        st.session_state.selected_restaurant_id = restaurant_id
                        
                        if menu_items:
                            show_order_dialog(menu_items, restaurant_id)
                        else:
                            st.warning("Este restaurante no tiene platillos disponibles.")
    




    st.markdown("---")
    
    
@st.dialog("Ordenar")
def show_order_dialog(menu_items, restaurant_id):
    total = 0
    order_items = []

    for item in menu_items:
        qty = st.number_input(
            f"{item['name']} - Q{item['price']}",
            min_value=0,
            step=1,
            key=f"qty_{item['_id']}"
        )

        if qty > 0:
            subtotal = qty * item['price']
            total += subtotal
            order_items.append({
                "menuItemId": item["_id"], 
                "quantity": qty,
                "price": item["price"]
            })

            st.caption(f"🛍️ {qty} x {item['name']} = Q{subtotal}")
            st.markdown("---")

    if total > 0:
        st.markdown(f"### 💰 Total: Q{total}")
        if st.button("🚚 Confirmar orden"):
            st.success("¡Orden enviada con éxito!")

            # Payload con nombres según schema
            order_payload = {
                "userId": st.session_state.user["id"],
                "restaurantId": restaurant_id,
                "items": order_items,
                "total": total
            }

            set_order(order_payload)
    else:
        st.info("Selecciona al menos un platillo para ordenar.")




