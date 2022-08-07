import streamlit as st
from constants import HIDE_STREAMLIT_STYLE
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


class Page:

    def __init__(self):
        self.hide_streamlit_default_layout()
        self.db = self.connect_to_db()

    @staticmethod
    @st.cache(allow_output_mutation=True)
    def connect_to_db():
        """
        Connect to postgres database containing users credentials.

        Returns
        -------

        """
        load_dotenv()

        db = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername='postgresql',
                username=os.getenv('USERNAME'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'),
                port=os.getenv('PORT'),
                database=os.getenv('DATABASE'),
            ),
            echo_pool=True,
        )

        base = declarative_base()
        base.metadata.create_all(db)
        return db

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
