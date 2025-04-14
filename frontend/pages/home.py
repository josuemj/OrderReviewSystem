import streamlit as st

def render():
    st.title("🍕 Panel Principal - Pizzabella")
    st.success(f"Bienvenido {st.session_state.user['name']} 👋")

    st.markdown("---")
    st.markdown("Aquí puedes navegar al panel de administración, restaurantes, menú, etc.")

    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
