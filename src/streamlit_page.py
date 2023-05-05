"""Parent class for all the pages of the app."""

import streamlit as st

from src.constants import HIDE_STREAMLIT_STYLE
from src.exceptions import WorksheetError
from src.google_sheet_connect import IndexSheet


class Page:
    """A class to manage the pages of the Streamlit App."""

    def __init__(self):
        """Initialize the class."""
        self.hide_streamlit_default_layout()
        self.sheet = None
        self.db = None
        self.map_cols = {
            "elecday": "Electricité Jour",
            "elecnight": "Electricité Nuit",
            "gas": "Gaz",
            "water": "Eau",
            "rainwater": "Eau de pluie",
            "elecday_consumption": "Electricité jour (kWh)",
            "elecnight_consumption": "Electricité nuit (kWh)",
            "gas_consumption": "Gaz (m3)",
            "water_consumption": "Eau (m3)",
            "rainwater_consumption": "Eau de pluie (m3)",
            "Year_consumption": "Année",
        }

    def check_auth(self):
        """Check if the user is connected."""
        st.markdown("## 🚨 Vous n'êtes pas connecté.")
        st.markdown("## 🚨 Veuillez vous connecter.")
        st.stop()

    def connect_to_gsheet(self):
        """
        Connect to the Google Sheet.

        Raises
        ------
        Exception
            If no sheet is found.
        """
        try:
            self.sheet = IndexSheet(sheet_name=st.session_state["user"])
            self.db = self.sheet.get_content_as_df()
        except WorksheetError:
            st.error("No sheet found")
            st.stop()

    def check_empty_db(self):
        """Check if the database is empty."""
        if self.db.empty:
            st.markdown(
                "## 🚨 Aucune donnée n'a été trouvée dans la base de données."
            )
            st.markdown("## 🚨 Veuillez remplir votre base de données.")
            st.stop()

    @staticmethod
    def hide_streamlit_default_layout():
        """Hide the default Streamlit menu."""
        st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)
