import streamlit as st
from streamlit_page import Page


st.set_page_config(layout="wide", page_title="Index", page_icon='📊',
                           initial_sidebar_state="expanded")


class Consumption(Page):
    def show_consumption_page(self):
        st.markdown("# Consommation")


if 'name' in st.session_state:
    app = Consumption()
    app.show_consumption_page()
else:
    st.info("Connectez-vous via la page d'accueil.")