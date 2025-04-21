import streamlit as st
from utils.api import get_orders_by_user, delete_order
from datetime import datetime

def render():
    st.title("Mis órdenes")
    st.text("Puede actualizar/eliminar una orden mientras su estatus sea pendiente")

    user_id = st.session_state.user["id"] # reemplazar con valor real o sesión
    orders = get_orders_by_user(user_id)

    if not orders:
        st.info("No tienes órdenes registradas.")
        return

    for order in orders:
        # Convertir fecha
        created_at = datetime.fromisoformat(order["createdAt"]).strftime("%d/%m/%Y %H:%M")
        status = order["status"]
        total = order["total"]

        with st.expander(f"📅 {created_at} | 🧾 Estado: {status} | 💰 Total: Q{total}"):
            st.markdown("### 🍕 Detalle del pedido:")
            for item in order["items"]:
                st.write(f"- **{item['name']}** — {item['quantity']} x Q{item['price']}")

            st.markdown("---")
            st.caption(f"🕒 Última actualización: {datetime.fromisoformat(order['updatedAt']).strftime('%d/%m/%Y %H:%M')}")

            if status == "pendiente":
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("❌ Cancelar", key=f"cancel_{order['_id']}"):
                        if delete_order(order_id=order["_id"]):
                            st.success("Orden cancelada correctamente")
                            st.rerun() 
                        else:
                            st.error("Error al cancelar la orden")
                        
                # with col2:
                #     if st.button("♻️ Actualizar", key=f"update_{order['_id']}"):
                #         st.info("Función actualizar aún no implementada") 