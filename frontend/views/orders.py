import streamlit as st
from utils.api import get_orders_by_user, delete_order, get_menu_items_by_restaurant, update_order
from datetime import datetime

def render():
    st.title("Mis órdenes")
    st.text("Puede actualizar/eliminar una orden mientras su estatus sea pendiente")

    user_id = st.session_state.user["id"] # reemplazar con valor real o sesión
    orders = get_orders_by_user(user_id)

    if not orders:
        st.info("No tienes órdenes registradas.")
        return
    st.subheader(f"Tienes {len(orders)} ordenes")
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
                        
                with col2:
                    if st.button("♻️ Actualizar", key=f"update_{order['_id']}"):
                        menu_items = get_menu_items_by_restaurant(order["restaurantId"])
                        show_update_order(order, menu_items)

@st.dialog("Actualizar Orden")
def show_update_order(order, menu_items):
    total = 0
    updated_items = []


    # Obtener cantidades actuales en un dict para lookup rápido
    current_quantities = {str(item["menuItemId"]): item["quantity"] for item in order["items"]}

    for item in menu_items:
        item_id_str = str(item["_id"])
        current_qty = current_quantities.get(item_id_str, 0)

        qty = st.number_input(
            f"{item['name']} - Q{item['price']}",
            min_value=0,
            step=1,
            value=current_qty,
            key=f"update_qty_{item_id_str}"
        )

        if qty > 0:
            subtotal = qty * item['price']
            total += subtotal
            updated_items.append({
                "menuItemId": item["_id"],
                "quantity": qty,
                "price": item["price"]
            })

            st.caption(f"🛍️ {qty} x {item['name']} = Q{subtotal}")
            st.markdown("---")

    if total > 0:
        st.markdown(f"### 💰 Total actualizado: Q{total}")
        if st.button("✅ Confirmar cambios"):
            
            update_payload = {
                "orderId": order["_id"],
                "items": updated_items,
                "total": total
            }
            
            if update_order(update_payload):
                st.success("Orden actualizada con éxito")
                st.rerun()
            else:
                st.error("Error al actualizar la orden")
    else:
        st.info("Selecciona al menos un platillo para actualizar.")
