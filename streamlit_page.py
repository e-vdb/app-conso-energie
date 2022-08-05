import streamlit as st
from constants import HIDE_STREAMLIT_STYLE


class Page:

    def __init__(self):
        self.hide_streamlit_default_layout()

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
