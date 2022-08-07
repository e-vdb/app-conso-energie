import streamlit as st
from streamlit_page import Page


st.set_page_config(layout="wide", page_title="Index", page_icon='🖋',
                           initial_sidebar_state="expanded")


class Index(Page):
    def show_index(self):
        st.markdown("# Gérer vos index")


if 'name' in st.session_state:
    app = Index()
    app.show_index()
else:
    st.info("Connectez-vous via la page d'accueil.")
