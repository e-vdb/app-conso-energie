import streamlit as st
from constants import HIDE_STREAMLIT_STYLE
from google_sheet_connect import get_df_from_sheet
from auth import check_password

class Page:

    def __init__(self):
        self.hide_streamlit_default_layout()
        self.db = get_df_from_sheet()
        self.map_cols = {'elecday': 'Electricité Jour',
                         'elecnight': 'Electricité Nuit',
                         'gas': 'Gaz',
                         'water': 'Eau',
                         'rainwater': 'Eau de pluie',
                         'elecday_consumption': 'Electricité jour (kWh)',
                         'elecnight_consumption': 'Electricité nuit (kWh)',
                         'gas_consumption': 'Gaz (m3)',
                         'water_consumption': 'Eau (m3)',
                         'rainwater_consumption': 'Eau de pluie (m3)',
                         'Year_consumption': 'Année'
                         }

    def check_auth(self):
        st.markdown("## 🚨 Vous n'êtes pas connecté.")
        st.markdown("## 🚨 Veuillez vous connecter.")
        st.stop()

    def check_empty_db(self):
        if self.db.empty:
            st.markdown("## 🚨 Aucune donnée n'a été trouvée dans la base de données.")
            st.markdown("## 🚨 Veuillez remplir votre base de données.")
            st.stop()

    @staticmethod
    def hide_streamlit_default_layout():
        st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

    def choose(self, options):
        st.sidebar.markdown("## 👉 Choose an action")
        """Display the different possible actions."""
        choice = st.sidebar.selectbox(
            label="What would you like to do?",
            options=options,
            help="You need to select what you'd like the application to do.",
        )
        return choice

    def show(self, possible_choices, callables) -> None:
        """
        Show the part of the app chosen by the user.

        Allow the user to navigate through a sidebar betweeen the different parts of the app.
        Call the appropriate function according to the action chosen by the user.
        Returns
        -------
        None
        """

        choice = self.choose(options=possible_choices)
        if choice is not None:
            args = [[], [], [], []]
            map_actions_to_callables = dict(zip(possible_choices, callables))

            # Calls the chosen function with relevant arguments
            map_actions_to_callables[choice](*args[0])
