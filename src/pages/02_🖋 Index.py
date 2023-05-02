import streamlit as st
from src.streamlit_page import Page
from src.constants import FRENCH_MONTHS
import pandas as pd
from datetime import datetime


st.set_page_config(
    layout="wide",
    page_title="Index",
    page_icon='🖋',
    initial_sidebar_state="expanded"
)


class Index(Page):

    CHOICES_INDEX = (
        "👁️ Visualiser vos index",
        "🖋️ Remplir vos index",
        "🖍️ Corriger vos relevés d'index"
    )

    def __init__(self):
        super(Index, self).__init__()
        self.connect_to_gsheet()
        self.last_index = self.sheet.get_last_row()["date"]
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

    def show_index(self):
        st.markdown("# Gérer vos index")
        callables = [
            self.visualise_index,
            self.fill_index,
            self.correct_index
        ]
        for count, tab in enumerate(st.tabs(self.CHOICES_INDEX)):
            with tab:
                callables[count]()

    def visualise_index(self):
        self.check_empty_db()
        st.table(self.db)

    def query_infos(self):
        row = {}
        row['ELECDAY'] = st.number_input(self.map_cols['elecday'])
        row['ELECNIGHT'] = st.number_input(self.map_cols['elecnight'])
        row['GAS'] = st.number_input(self.map_cols['gas'])
        row['WATER'] = st.number_input(self.map_cols['water'])
        row['RAINWATER'] = st.number_input(self.map_cols['rainwater'])
        return row

    def fill_index(self):
        if datetime.strptime(self.last_index, "%Y-%m-%d").month == datetime.now().month:
            st.warning(
                "Vous avez déjà rempli vos index pour ce mois-ci. "
                "Rendez-vous au début du mois prochain."
            )
            st.stop()
        else:
            st.info("Remplissez vos index pour ce mois-ci.")

        index_date = datetime(
            year=datetime.now().year,
            month=datetime.now().month,
            day=1
        )
        index_date = datetime.strftime(index_date, "%Y-%m-%d")
        indexes = list(self.query_infos().values())
        content = [index_date, *indexes]

        if st.button("Ajouter"):
            self.sheet.add_row_to_sheet(list(content))
            st.success("Index ajouté !")

    def correct_index(self):
        self.check_empty_db()


app = Index()
if st.session_state["authenticated"]:
    app.show_index()
else:
    app.check_auth()

