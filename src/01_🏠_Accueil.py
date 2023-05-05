"""Home page of the app."""

# flake8: noqa: E402
# pylint: disable=wrong-import-position, import-error
# pylint: disable=invalid-name, non-ascii-file-name, super-with-arguments

import os
import sys

import streamlit as st

# Add app directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# pylint: enable=wrong-import-position

from auth import check_password
from constants import DESCRIPTION
from src.streamlit_page import Page

st.set_page_config(
    layout="wide",
    page_title="Home",
    page_icon="🏠",
    initial_sidebar_state="expanded",
)


class Home(Page):
    """A class to manage the home page of the Streamlit App."""

    def authenticate_user(self):
        """
        Grant access to the app if the user is authenticated.

        Check the user's credentials.
        Connect to the Google Sheet.
        Display the home page.
        """
        if check_password():
            st.session_state["authenticated"] = True
            st.write(f"Welcome back {st.session_state['username']}")
            st.session_state["user"] = st.session_state["username"]
            st.success("🔓 Authentification réussie !")
            self.show_home()
            self.connect_to_gsheet()

    @staticmethod
    def show_home():
        """Display the home page."""
        st.markdown("# Accueil")
        st.write(DESCRIPTION)


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

app = Home()
if st.session_state["authenticated"]:
    app.show_home()
else:
    app.authenticate_user()
