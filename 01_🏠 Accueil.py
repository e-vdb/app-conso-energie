import streamlit as st
from streamlit_page import Page
from streamlit import cli as stcli
import sys

st.set_page_config(layout="wide", page_title="Home", page_icon='🏠',
                           initial_sidebar_state="expanded")


class Home(Page):
    @staticmethod
    def show_home():
        st.markdown("# Accueil")


def main():
    app = Home()
    app.show_home()


if __name__ == "__main__":
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())