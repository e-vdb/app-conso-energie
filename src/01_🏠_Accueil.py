import streamlit as st

from streamlit_page import Page
from constants import DESCRIPTION
from auth import check_password

st.set_page_config(layout="wide", page_title="Home", page_icon='🏠',
                           initial_sidebar_state="expanded")


class Home(Page):
    def __init__(self):
        super(Home, self).__init__()

    def authenticate_user(self):
        if check_password():
            st.session_state["authenticated"] = True
            st.success("🔓 Authentification réussie !")
            self.show_home()

    @staticmethod
    def show_home():
        st.markdown("# Accueil")
        st.write(DESCRIPTION)


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

app = Home()
if st.session_state["authenticated"]:
    app.show_home()
else:
    app.authenticate_user()
