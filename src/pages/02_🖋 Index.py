"""App page to manage the index of the electricity, water and gas meters."""

# pylint: disable=invalid-name, non-ascii-file-name, super-with-arguments

import logging
from datetime import datetime

import streamlit as st

from src.exceptions import NoIndexRecordedYet
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

        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

    def fetch_last_index(self):
        """Fetch the last index recorded."""
        try:
            return self.sheet.get_last_row()
        except IndexError as exc:
            raise NoIndexRecordedYet from exc

    def show_index(self):
        """Show the index page."""
        st.markdown("# Gérer vos index")
        callables = [self.visualise_index, self.fill_index, self.correct_index]
        for count, tab in enumerate(st.tabs(self.CHOICES_INDEX)):
            with tab:
                callables[count]()

    def visualise_index(self):
        """Visualise the index table."""
        self.check_empty_db(stop=False)
        st.table(self.db)

    def show_inputs_index_widgets(  # pylint: disable=too-many-arguments
        self,
        elecday_min: float = 0.0,
        elecnight_min: float = 0.0,
        gas_min: float = 0.0,
        water_min: float = 0.0,
        rainwater_min: float = 0.0,
        tab: str = "fill_index",
    ) -> dict:
        """Allow the user to fill the index."""
        return {
            "ELECDAY": st.number_input(
                label=self.map_cols["elecday"],
                key=f"{tab}_elecday",
                min_value=elecday_min,
            ),
            "ELECNIGHT": st.number_input(
                label=self.map_cols["elecnight"],
                key=f"{tab}_elecnight",
                min_value=elecnight_min,
            ),
            "GAS": st.number_input(
                label=self.map_cols["gas"], key=f"{tab}_gas", min_value=gas_min
            ),
            "WATER": st.number_input(
                label=self.map_cols["water"],
                key=f"{tab}_water",
                min_value=water_min,
            ),
            "RAINWATER": st.number_input(
                label=self.map_cols["rainwater"],
                key=f"{tab}_rainwater",
                min_value=rainwater_min,
            ),
        }

    def fill_index(self):
        """Ask the user to fill the index."""
        try:
            last_index = self.fetch_last_index()
            if (
                datetime.strptime(last_index["date"], "%Y-%m-%d").month
                == datetime.now().month
            ):
                st.warning(
                    "Vous avez déjà rempli vos index pour ce mois-ci. "
                    "Rendez-vous au début du mois prochain."
                )
            else:
                st.info("Remplissez vos index pour ce mois-ci.")

                index_date = datetime(
                    year=datetime.now().year, month=datetime.now().month, day=1
                )
                index_date = datetime.strftime(index_date, "%Y-%m-%d")
                indexes = list(
                    self.show_inputs_index_widgets(
                        elecday_min=last_index["elecday"],
                        elecnight_min=last_index["elecnight"],
                        gas_min=last_index["gas"],
                        water_min=last_index["water"],
                        rainwater_min=last_index["rainwater"],
                        tab="fill_index",
                    ).values()
                )
                content = [index_date, *indexes]

                if st.button("Ajouter"):
                    self.sheet.add_row_to_sheet(list(content))
                    st.success("Index ajouté !")
        except NoIndexRecordedYet:
            st.warning("Aucun index n'a été enregistré pour le moment.")
            index_date = datetime(
                year=datetime.now().year, month=datetime.now().month, day=1
            )
            index_date = datetime.strftime(index_date, "%Y-%m-%d")
            indexes = list(self.show_inputs_index_widgets().values())
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

        new_values = list(
            self.show_inputs_index_widgets(
                tab="correct_index",
            ).values()
        )
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
