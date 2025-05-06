import streamlit as st
from utils.api import get_all_restaurants, get_pending_orders_by_restaurant, bulk_update_orders_by_restaurant

def render():
    estados = ["pendiente", "en preparación", "entregado"]

    st.title("📦 Gestión de órdenes por restaurante")

    restaurants = get_all_restaurants()
    if not restaurants:
        st.warning("No hay restaurantes disponibles.")
        st.stop()

    restaurant_options = {r["name"]: r["_id"] for r in restaurants}
    selected_name = st.selectbox("Selecciona un restaurante", ["-- Selecciona --"] + list(restaurant_options.keys()))

    if selected_name != "-- Selecciona --":
        selected_id = restaurant_options[selected_name]
        pending_orders = get_pending_orders_by_restaurant(selected_id)

        if not pending_orders:
            st.info("🎉 No hay órdenes pendientes.")
        else:
            st.write(f"Órdenes pendientes encontradas: `{len(pending_orders)}`")

            estado_local = {}  # Guarda cambios

            for order in pending_orders:
                order_id = order["_id"]
                current_status = order.get("status", "pendiente")

                with st.expander(f"🧾 Orden #{order_id} - Estado actual: {current_status}"):
                    new_status = st.selectbox(
                        f"Nuevo estado para orden #{order_id}",
                        estados,
                        index=estados.index(current_status),
                        key=f"estado_{order_id}"
                    )
                    estado_local[order_id] = new_status

            # 🔘 Botón global para aplicar todos los cambios
            if st.button("✅ Actualizar órdenes"):
                updates = []
                for oid, new_status in estado_local.items():
                    original = next((o for o in pending_orders if o["_id"] == oid), {})
                    if original.get("status") != new_status:
                        updates.append({"orderId": oid, "status": new_status})

                if updates:
                    updated_count = bulk_update_orders_by_restaurant(selected_id, updates)
                    st.success(f"Se actualizaron {updated_count} órdenes.")
                    st.rerun()
                else:
                    st.info("No hiciste ningún cambio.")
