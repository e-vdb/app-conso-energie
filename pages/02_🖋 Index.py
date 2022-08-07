import streamlit as st
from streamlit_page import Page
from constants import CHOICES_INDEX

st.set_page_config(layout="wide", page_title="Index", page_icon='🖋',
                           initial_sidebar_state="expanded")


class Index(Page):

    def show_index(self):
        st.markdown("# Gérer vos index")
        callables = [self.visualise_index, self.fill_index, self.correct_index]
        self.show(possible_choices=CHOICES_INDEX, callables=callables)

    def visualise_index(self):
        pass

    def fill_index(self):
        pass

    def correct_index(self):
        pass


if 'name' in st.session_state:
    app = Index()
    app.show_index()
else:
    st.info("Connectez-vous via la page d'accueil.")
