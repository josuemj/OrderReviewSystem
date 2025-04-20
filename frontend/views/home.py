import streamlit as st
from utils.api import get_all_restaurants, get_top_rated_restaurants, get_avg_rating_by_restaurant, get_menu_items_by_restaurant
import pandas as pd

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
        
        if st.button("Ordenar"):
            restaurants = get_all_restaurants()
            st.session_state.restaurants = restaurants
            st.session_state.view = "order"

    with col2:
        if st.button("⭐ Ver mejores calificados"):
            top_restaurants = get_top_rated_restaurants()
            st.session_state.restaurants = top_restaurants
            st.session_state.view = "top"

    st.markdown("---")
    if "restaurants" in st.session_state:
        view_label = "Todos los restaurantes" if st.session_state.view == "all" else "Mejores calificados"
        view_label = "Ordenar" if st.session_state.view == "order" else view_label
        st.subheader(view_label)

        for r in st.session_state.restaurants:
            
            print(type(r))
            print(r)
            restaurant_id =  r["_id"]
            lat = r["location"]["coordinates"]["lat"]
            lon = r["location"]["coordinates"]["lng"]
            
            with st.expander(f"{r['name']}"):

                st.markdown(f"📍 Ubicación: {r["location"]["address"]}")
                st.markdown(f"🌆 City {r["location"]["city"]}")
                st.markdown(f"🏷️ Categorías: {', '.join(r.get('categories', []))}")
                
                if view_label == "Todos los restaurantes":
                    details = get_avg_rating_by_restaurant(r['_id']) or {}
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
                            show_order_dialog(menu_items)
                        else:
                            st.warning("Este restaurante no tiene platillos disponibles.")
    




    st.markdown("---")
    
    
@st.dialog("Ordernar")
def show_order_dialog(menu_items):
    total = 0
    order = []

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
            order.append({
                "item_id": item["_id"],
                "name": item["name"],
                "price": item["price"],
                "qty": qty,
                "subtotal": subtotal
            })

            st.caption(f"🛍️ {qty} x {item['name']} = Q{subtotal}")
            st.markdown("---")

    if total > 0:
        st.markdown(f"### 💰 Total: Q{total}")
        if st.button("🚚 Confirmar orden"):
            # Aquí podrías guardar la orden o simularla
            st.success("¡Orden enviada con éxito!")
    else:
        st.info("Selecciona al menos un platillo para ordenar.")


