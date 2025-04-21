import streamlit as st
from session_state import init_session
from views import login, home, orders, reviews, profile

# Inicializa variables de sesión
init_session()

def main():
    if st.session_state.logged_in:
        if st.session_state.user["name"] != "admin":
            # Solo mostrar sidebar si está logueado
            st.sidebar.title("🍕 Navegación")
            selected = st.sidebar.radio("Ir a:", ["🏠 Home", "📦 Órdenes", "📝 Reseñas", "👤 Perfil"])

            if selected == "🏠 Home":
                home.render()
            elif selected == "📦 Órdenes":
                orders.render()
            elif selected == "📝 Reseñas":
                reviews.render()
            elif selected == "👤 Perfil":
                profile.render()

            if st.sidebar.button("Cerrar sesión", key="logout_sidebar"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
        else:
            
            selected = st.sidebar.radio("Ir a:", ["🏠 Restaurantes", "📦 Órdenes", "📝 Stats"])

            if selected == "🏠 Restaurantes":
                st.title("Gestionar restaurantes")
                st.text("CRUD restaurante")
            elif selected == "📦 Órdenes":
                st.title("Gestor de ordenes")
                st.text("Cambiar de estado ordenes")
            elif selected == "📝 Stats":
                st.title("Stats")
                st.text("Stas ventas platillos etc")
                
            if st.sidebar.button("Cerrar sesión", key="logout_sidebar"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
    else:
        # No mostrar sidebar si no ha iniciado sesión
        login.render()

if __name__ == "__main__":
    main()
