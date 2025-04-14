import streamlit as st
from utils.api import authenticate_user

def render():
    st.markdown("""
        <h1 style='text-align: center; color: #D2691E;'>🍽️ Bienvenido a Pizzabella</h1>
        <h4 style='text-align: center; color: #8B0000;'>¡Tu destino para descubrir los mejores restaurantes y ordenar platillos deliciosos!</h4>
        <hr>
    """, unsafe_allow_html=True)

    st.subheader("Inicia sesión para continuar")

    with st.form("login_form"):
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")

        if submit:
            user = authenticate_user(email=email, password=password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success("Inicio de sesión exitoso. Redirigiendo...")
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
