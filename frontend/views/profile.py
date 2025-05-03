import streamlit as st

def render():
    st.title("👤 Perfil del Usuario")

    user = st.session_state.get("user")

    if not user:
        st.warning("No se ha encontrado el usuario en sesión.")
        return

    st.subheader("Información Personal")
    st.text_input("Nombre", value=user["name"], disabled=True)
    st.text_input("Email", value=user["email"], disabled=True)

    st.markdown("---")
    st.subheader("📦 Órdenes")
    total_orders = len(user.get("orders", []))
    st.metric(label="Órdenes realizadas", value=total_orders)
