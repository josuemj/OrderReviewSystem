import streamlit as st
from session_state import init_session
from pages import login, home  # puedes tener más vistas aquí

# Inicializa variables
init_session()

def main():
    if st.session_state.logged_in:
        home.render()
    else:
        login.render()

if __name__ == "__main__":
    main()
