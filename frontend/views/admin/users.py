import streamlit as st
from utils.api import get_all_users, update_user as api_update_user, delete_user, get_orders_by_user

def render():
    st.title("👤 Gestión de Usuarios")

    # Parámetros de paginación
    page = st.session_state.get("users_page", 1)
    limit = 10

    st.markdown("### 📋 Lista de Usuarios")
    users = get_all_users(page=page, limit=limit)

    if not users:
        st.info("No hay usuarios registrados.")
        return

    for user in users:
        with st.expander(f"{user['name']} - {user['email']}"):
            st.write(f"📧 Email: {user['email']}")
            st.write(f"🆔 ID: {user['id']}")
            orders = get_orders_by_user(user["id"])
            st.write(f"🛒 Órdenes: {len(orders)}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Editar", key=f"edit_{user['id']}"):
                    st.session_state.user_to_edit = user
                    show_edit_dialog()

            with col2:
                if st.button("🗑️ Eliminar", key=f"delete_{user['id']}"):
                    st.session_state.user_to_delete = user
                    show_delete_dialog()

    st.divider()

    # Paginación
    col1, col2, _ = st.columns([1, 1, 4])
    with col1:
        if page > 1 and st.button("⬅️ Anterior"):
            st.session_state.users_page = page - 1
            st.rerun()
    with col2:
        if len(users) == limit and st.button("➡️ Siguiente"):
            st.session_state.users_page = page + 1
            st.rerun()


@st.dialog("Editar Usuario")
def show_edit_dialog():
    user = st.session_state.get("user_to_edit")
    if not user:
        st.warning("Usuario no encontrado.")
        return

    name = st.text_input("Nombre", value=user["name"])
    email = st.text_input("Correo", value=user["email"])
    password = st.text_input("Nueva contraseña", type="password", placeholder="Dejar en blanco para no cambiar")

    if st.button("Guardar cambios"):
        data = {"name": name, "email": email}
        if password:
            data["password"] = password  # La API debe recibir esto y volverlo hash

        success = api_update_user(user["id"], data)
        if success:
            st.success("Usuario actualizado correctamente.")
            st.rerun()
        else:
            st.error("No se pudo actualizar al usuario.")

@st.dialog("Confirmar eliminación")
def show_delete_dialog():
    user = st.session_state.get("user_to_delete")
    if not user:
        st.warning("No se encontró el usuario a eliminar.")
        return

    st.warning(f"¿Estás seguro que deseas eliminar a **{user['name']}**?\n\nEsto eliminará también sus órdenes y reseñas.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Cancelar"):
            st.session_state.user_to_delete = None
            st.rerun()
    with col2:
        if st.button("✅ Sí, eliminar"):
            success = delete_user(user["id"])
            st.session_state.user_to_delete = None
            if success:
                st.success("Usuario eliminado.")
                st.rerun()
            else:
                st.error("Error al eliminar el usuario.")
