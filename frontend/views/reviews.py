import streamlit as st
from utils.api import get_all_reviews, create_review, update_review, delete_review
from datetime import datetime

def render():
    st.title("📝 Mis Reseñas")

    user_id = st.session_state.user.get("id")

    if not user_id:
        st.warning("No se ha encontrado el usuario.")
        return

    if "review_page" not in st.session_state:
        st.session_state.review_page = 1

    if st.button("➕ Nueva Reseña"):
        with st.modal("Crear Reseña"):
            form_review(None, user_id)

    st.markdown("---")
    st.subheader("📋 Tus Reseñas")

    reviews = get_all_reviews(st.session_state.review_page, user_id=user_id)

    if not reviews:
        st.info("No hay reseñas para mostrar.")
        return

    for review in reviews:
        with st.expander(f"{review.get('comment', '')} - ⭐ {review['rating']}"):
            st.write(f"📍 Restaurante: {review.get('restaurantId', 'N/D')}")
            st.write(f"✍️ Rating: {review.get('rating', '')}")
            st.write(f"🕒 Fecha: {review.get('createdAt', '')[:10]}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Editar", key=f"edit_{review['id']}"):
                    form_review(review, user_id)

            with col2:
                if st.button("🗑️ Eliminar", key=f"delete_{review['id']}"):
                    st.session_state.review_to_delete = review
                    confirm_delete_dialog()

    st.markdown("---")
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Anterior") and st.session_state.review_page > 1:
            st.session_state.review_page -= 1
            st.rerun()
    with col2:
        if len(reviews) == 10:
            if st.button("Siguiente ➡️"):
                st.session_state.review_page += 1
                st.rerun()

@st.dialog("Edita tu review ⭐")
def form_review(review, user_id):
    is_edit = review is not None

    st.text(f"🧾 ID de la Orden: {review['orderId']}")
    st.text(f"🍽️ ID del Restaurante: {review['restaurantId']}")
    comment = st.text_input("Commentario", value=review["comment"] if is_edit else "")
    rating = st.slider("Calificación (1-5)", min_value=1.0, max_value=5.0, value=review["rating"] if is_edit else 5.0)

    if st.button("Guardar"):
        data = {
            "userId": user_id,
            "comment": comment,
            "orderId": review['orderId'],
            "rating": rating,
            "restaurantId": review['restaurantId'],
        }

        if is_edit:
            result = update_review(review["id"], data)
            if result:
                st.success("Reseña actualizada.")
                st.rerun()
            else:
                st.error("No se pudo actualizar.")
        else:
            result = create_review(data)
            if result:
                st.success("Reseña creada.")
                st.rerun()
            else:
                st.error("No se pudo crear la reseña.")

@st.dialog("Confirmar eliminación")
def confirm_delete_dialog():
    review = st.session_state.get("review_to_delete")
    if not review:
        st.warning("No se encontró la reseña a eliminar.")
        return

    st.warning(f"¿Estás seguro que deseas eliminar esta reseña?\n\n✍️ {review.get('comment', '')}\n\n🧾 ID de la Orden: {review['orderId']}\n\n🍽️ ID del Restaurante: {review['restaurantId']}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Cancelar"):
            st.session_state.review_to_delete = None
            st.rerun()
    with col2:
        if st.button("✅ Sí, eliminar"):
            success = delete_review(review["id"])
            st.session_state.review_to_delete = None
            if success:
                st.success("Reseña eliminada.")
                st.rerun()
            else:
                st.error("Error al eliminar la reseña.")