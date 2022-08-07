import streamlit as st
from streamlit import cli as stcli
import sys


from user_db import UserDatabase
from streamlit_authenticator import StreamlitAuthenticator
from streamlit_page import Page
from constants import DESCRIPTION


st.set_page_config(layout="wide", page_title="Home", page_icon='🏠',
                           initial_sidebar_state="expanded")


class Home(Page):
    def __init__(self):
        super(Home, self).__init__()
        self.user_db = UserDatabase(self.db)
        USERS_TABLE = self.user_db.return_table_as_df()
        self.authenticator = StreamlitAuthenticator(USERS_TABLE)

    def authentication(self):
        self.authenticator.authentication(main_app_fct_to_show=self.show_home)

    @staticmethod
    def show_home():
        st.markdown("# Accueil")
        st.write(f"Bienvenue {st.session_state['name']}")
        st.write(DESCRIPTION)


def main():
    app = Home()
    app.authentication()


if __name__ == "__main__":
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
