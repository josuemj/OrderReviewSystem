import streamlit as st
from utils.api import upload_file_to_collection, download_collection_file
import tempfile

def render():
    st.title("📂 Gestión de Archivos de Base de Datos")
    st.write("Aquí puedes descargar datos de restaurants, menu_item, orders, users, reviews.")

    st.header("⬇️ Descargar colección")
    download_collection = st.text_input("Nombre de la colección a descargar:", key="download_collection")
    download_format = st.selectbox("Formato de descarga:", options=["json", "csv", "bson"], key="download_format")

    if st.button("Descargar colección"):
        if download_collection and download_format:
            result = download_collection_file(download_collection, download_format)
            if result["success"]:
                st.success(f"Archivo descargado exitosamente en: {result['path']}")
                with open(result["path"], "rb") as f:
                    st.download_button(
                        label="Descargar Archivo",
                        data=f,
                        file_name=result["path"].split("/")[-1],
                        mime="application/octet-stream"
                    )
            else:
                st.error(f"Error descargando colección: {result['detail']}")
        else:
            st.warning("Debes ingresar nombre de colección y formato de descarga.")
