import streamlit as st
from streamlit_page import Page
from constants import CHOICES_CONSOMMATION

st.set_page_config(layout="wide", page_title="Index", page_icon='📊',
                           initial_sidebar_state="expanded")


class Consumption(Page):
    def show_consumption_page(self):
        st.markdown("# Consommation")
        callables = [self.calculate_total_consumption, self.calculate_monthly_consumption,
                     self.compare_with_previous_consumption]
        self.show(possible_choices=CHOICES_CONSOMMATION, callables=callables)

    def calculate_total_consumption(self):
        pass

    def calculate_monthly_consumption(self):
        pass

    def compare_with_previous_consumption(self):
        pass



if 'name' in st.session_state:
    app = Consumption()
    app.show_consumption_page()
else:
    st.info("Connectez-vous via la page d'accueil.")