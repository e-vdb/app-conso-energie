"""App page to manage the index of the electricity, water and gas meters."""

# pylint: disable=invalid-name, non-ascii-file-name, super-with-arguments

import logging
from datetime import datetime

import streamlit as st

from src.streamlit_page import Page

st.set_page_config(
    layout="wide",
    page_title="Index",
    page_icon="🖋",
    initial_sidebar_state="expanded",
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Index(Page):
    """A class to manage the index page."""

    CHOICES_INDEX = (
        "👁️ Visualiser vos index",
        "🖋️ Remplir vos index",
        "🖍️ Corriger vos relevés d'index",
    )

    def __init__(self):
        """Initialize the class."""
        super(Index, self).__init__()
        self.connect_to_gsheet()
        self.last_index = self.sheet.get_last_row()["date"]
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

    def show_index(self):
        """Show the index page."""
        st.markdown("# Gérer vos index")
        callables = [self.visualise_index, self.fill_index, self.correct_index]
        for count, tab in enumerate(st.tabs(self.CHOICES_INDEX)):
            with tab:
                callables[count]()

    def visualise_index(self):
        """Visualise the index table."""
        self.check_empty_db()
        st.table(self.db)

    def query_infos(self):
        """Allow the user to fill the index."""
        row = {}
        row["ELECDAY"] = st.number_input(self.map_cols["elecday"])
        row["ELECNIGHT"] = st.number_input(self.map_cols["elecnight"])
        row["GAS"] = st.number_input(self.map_cols["gas"])
        row["WATER"] = st.number_input(self.map_cols["water"])
        row["RAINWATER"] = st.number_input(self.map_cols["rainwater"])
        return row

    def fill_index(self):
        """Ask the user to fill the index."""
        if (
            datetime.strptime(self.last_index, "%Y-%m-%d").month
            == datetime.now().month
        ):
            st.warning(
                "Vous avez déjà rempli vos index pour ce mois-ci. "
                "Rendez-vous au début du mois prochain."
            )
            # st.stop()
        else:
            st.info("Remplissez vos index pour ce mois-ci.")

            index_date = datetime(
                year=datetime.now().year, month=datetime.now().month, day=1
            )
            index_date = datetime.strftime(index_date, "%Y-%m-%d")
            indexes = list(self.query_infos().values())
            content = [index_date, *indexes]

            if st.button("Ajouter"):
                self.sheet.add_row_to_sheet(list(content))
                st.success("Index ajouté !")

    def correct_index(self):
        """Allow the user to correct the index."""
        self.check_empty_db()
        selected_date = st.selectbox(
            label="Choisissez la ligne à corriger", options=self.db["date"]
        )
        st.info("Remplissez les index corrects.")
        row_to_correct = self.db[self.db["date"] == selected_date]
        st.table(row_to_correct)

        new_values = list(self.query_infos().values())
        new_content = [selected_date, *new_values]

        if st.button("Corriger"):
            index_to_correct = row_to_correct.index[0]
            self.sheet.update_row_in_sheet(index_to_correct + 2, new_content)
            st.success("Index corrigés !")


app = Index()
if st.session_state["authenticated"]:
    app.show_index()
else:
    app.check_auth()
