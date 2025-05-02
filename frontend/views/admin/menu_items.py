import streamlit as st
from utils.api import get_all_menu_items

def render():
    st.title("🧾 Gestión de platillos")

    st.markdown("### Selecciona una acción")
    opcion = st.radio(
        "Opciones disponibles:",
        (
            "📋 Ver todos los platillos",
            "➕ Crear platillo",
            "🗑️ Eliminar platillo",
            "✏️ Actualizar platillo"
        )
    )

    st.markdown("---")

    # Ver platillos
    if opcion == "📋 Ver todos los platillos":
        st.subheader("Listado completo de platillos")

        platillos = get_all_menu_items()
        if not platillos:
            st.info("No hay platillos disponibles.")
        else:
            st.success(f"Se encontraron {len(platillos)} platillos.")
            for p in platillos:
                with st.expander(p["name"]):
                    st.markdown(f"📝 **Descripción:** {p.get('description', 'Sin descripción')}")
                    st.markdown(f"💰 **Precio:** Q{p.get('price', 'No especificado')}")
                    st.image(p["image"], width=200)
                    st.caption(f"🕒 Creado: {p.get('createdAt')}")
                    st.caption(f"🔄 Actualizado: {p.get('updatedAt')}")
