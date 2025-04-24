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
                    with st.modal("Editar Reseña"):
                        form_review(review, user_id)

            with col2:
                if st.button("🗑️ Eliminar", key=f"delete_{review['id']}"):
                    if st.confirm("¿Estás seguro que deseas eliminar esta reseña?"):
                        success = delete_review(review["id"])
                        if success:
                            st.success("Reseña eliminada.")
                            st.rerun()
                        else:
                            st.error("Error al eliminar la reseña.")

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

def form_review(review, user_id):
    is_edit = review is not None

    title = st.text_input("Título", value=review["title"] if is_edit else "")
    content = st.text_area("Contenido", value=review["content"] if is_edit else "")
    rating = st.slider("Calificación (1-5)", min_value=1, max_value=5, value=review["rating"] if is_edit else 5)
    restaurant_id = st.text_input("ID del Restaurante", value=review["restaurantId"] if is_edit else "")

    if st.button("Guardar"):
        data = {
            "userId": user_id,
            "title": title,
            "content": content,
            "rating": rating,
            "restaurantId": restaurant_id,
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
