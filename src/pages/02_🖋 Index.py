import streamlit as st
from streamlit_page import Page
from constants import CHOICES_INDEX

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

    def fill_index(self):
        pass

    def correct_index(self):
        self.check_empty_db()


app = Index()
if st.session_state["authenticated"]:
    app.show_index()
else:
    app.check_auth()

