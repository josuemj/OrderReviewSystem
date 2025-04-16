import streamlit as st
from session_state import init_session
from views import login, home, orders, reviews, profile

# Inicializa variables de sesión
init_session()

def main():
    if st.session_state.logged_in:
        # Solo mostrar sidebar si está logueado
        st.sidebar.title("🍕 Navegación")
        selected = st.sidebar.radio("Ir a:", ["🏠 Home", "📦 Mis Órdenes", "📝 Mis Reseñas", "👤 Mi Perfil"])

        if selected == "🏠 Home":
            home.render()
        elif selected == "📦 Mis Órdenes":
            orders.render()
        elif selected == "📝 Mis Reseñas":
            reviews.render()
        elif selected == "👤 Mi Perfil":
            profile.render()

        if st.sidebar.button("Cerrar sesión", key="logout_sidebar"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    else:
        # No mostrar sidebar si no ha iniciado sesión
        login.render()

if __name__ == "__main__":
    main()
