import streamlit as st
from utils.api import authenticate_user, register_user

def render():
    st.markdown("""
        <h1 style='text-align: center; color: #D2691E;'>🍽️ Bienvenido a Pizzabella</h1>
        <h4 style='text-align: center; color: #8B0000;'>¡Tu destino para descubrir los mejores restaurantes y ordenar platillos deliciosos!</h4>
        <hr>
    """, unsafe_allow_html=True)

    st.subheader("Inicia sesión para continuar")

    # login
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
                
    # registro
    with st.expander("¿No tienes cuenta? Regístrate aquí"):
        with st.form("register_form"):
            name = st.text_input("Nombre")
            new_email = st.text_input("Correo electrónico (nuevo)")
            new_password = st.text_input("Contraseña (nueva)", type="password")
            register_submit = st.form_submit_button("Registrarse")

            if register_submit:
                if not name.strip() or not new_email.strip() or not new_password.strip():
                    st.warning("Por favor, completa todos los campos antes de registrarte.")
                else:
                    response = register_user(name, new_email, new_password)
                    if response["success"]:
                        st.success("✅ Registro exitoso. Ahora puedes iniciar sesión.")
                    else:
                        st.error(f"❌ Error al registrarse: {response['detail']}")

