import streamlit as st
from streamlit import cli as stcli
import sys
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

from user_db import UserDatabase
from streamlit_authenticator import StreamlitAuthenticator
from streamlit_page import Page

st.set_page_config(layout="wide", page_title="Home", page_icon='🏠',
                           initial_sidebar_state="expanded")


class Home(Page):
    def __init__(self):
        super(Home, self).__init__()
        self.db = self.connect_to_db()
        self.user_db = UserDatabase(self.db)
        USERS_TABLE = self.user_db.return_table_as_df()
        self.authenticator = StreamlitAuthenticator(USERS_TABLE)

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

    def authentication(self):
        self.authenticator.authentication(main_app_fct_to_show=self.show_home)

    @staticmethod
    def show_home():
        st.markdown("# Accueil")
        st.write(f"Bienvenue {st.session_state['name']}")


def main():
    app = Home()
    app.authentication()


if __name__ == "__main__":
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())