import streamlit as st
from streamlit_page import Page
from consumption import ConsumptionDataframe
from frontend import plot_consumption, dic_name

st.set_page_config(
    layout="wide",
    page_title="Consommation totale",
    page_icon='📊',
    initial_sidebar_state="expanded"
)


class Consumption(Page):

    CHOICES_CONSOMMATION = (
        "📊 Consommation totale",
        "📊 Consommation annuelle",
        "🟩 Comparaison consommation 🟥",
    )

    def __init__(self):
        super(Consumption, self).__init__()
        self.check_empty_db()
        self.consumption = ConsumptionDataframe(self.db)
        self.consumption.evaluate_consumption()
        self._list_years = self.identify_years()

    def identify_years(self):
        return [i for i in range(
                    self.consumption.df['date'].dt.year.min(),
                    self.consumption.df['date'].dt.year.max() + 1
                    )
                ]

    def show_consumption_page(self):
        """Allow the user to navigate in Consumption page."""
        st.markdown("# Consommation")

        callables = [
            self.calculate_total_consumption,
            self.calculate_monthly_consumption,
            self.compare_with_previous_consumption
        ]

        for count, tab in enumerate(st.tabs(self.CHOICES_CONSOMMATION)):
            with tab:
                callables[count]()


    def check_empty_data(self):
        if self.consumption.df.empty:
            st.warning("Aucune donnée stockée. Remplissez d'abord vos index.")
            st.stop()

    def calculate_total_consumption(self):
        """Compute and display total consumption."""
        # Compute yearly consumption
        cols = self.consumption.consumption_columns[1:]
        tot_cons_per_year = self.consumption.df.groupby('Year_consumption')[
            cols].sum()
        tot_cons_per_year = tot_cons_per_year.reset_index()

        # Charts
        fig_years = plot_consumption(
            tot_cons_per_year, 'Year_consumption',
            cols
        )

        # Rename columns
        tot_cons_per_year.rename(columns=self.map_cols, inplace=True)

        for fig in fig_years:
            st.plotly_chart(fig, use_container_width=True)
        st.table(tot_cons_per_year)

    def calculate_monthly_consumption(self):
        """Compute and display monthly consumption."""
        selected_year = st.selectbox(
            label='Année',
            options=self._list_years,
            help="Choisissez l'année pour laquelle vous souhaitez voir les consommations mensuelles"
        )

        # Monthly consumption graphics

        st.subheader(f"Consommation pour l'année {selected_year}")
        df_filter = self.consumption.filter_year(str(selected_year))
        cols = self.consumption.consumption_columns[1:]
        fig_selected_year = plot_consumption(df_filter, 'Month_consumption',
                                             cols)
        for fig in fig_selected_year:
            st.plotly_chart(fig, use_container_width=True)

    def compare_with_previous_consumption(self):
        year1 = st.selectbox(
            label='Année',
            options=self._list_years[1:],
            help="Choisissez l'année pour laquelle vous souhaitez comparer les consommations mensuelles"
        )

        df_year = self.consumption.df.groupby('Year_consumption')
        saved_cols = list(self.consumption.saved_columns)
        df1 = df_year.get_group(year1).drop(
            [*saved_cols, 'date_consumption', 'Year_consumption'], axis=1)
        df1.set_index('Month_consumption', inplace=True)
        df1.rename(columns=dic_name, inplace=True)
        index = self._list_years.index(year1)
        for year2 in self._list_years[0:index]:
            df2 = df_year.get_group(year2).drop(
                [*saved_cols, 'date_consumption', 'Year_consumption'], axis=1)
            df2.set_index('Month_consumption', inplace=True)
            df2.rename(columns=dic_name, inplace=True)
            st.subheader(f'Comparaison entre {year1} et {year2}')
            diff = (df1 - df2).dropna(axis=0)
            cols = [col for col in diff.columns if (diff[col] != 0).all()]
            diff = diff[cols]
            st.dataframe(
                diff.style.background_gradient(axis=0, cmap='RdYlGn_r'))


app = Consumption()

if st.session_state["authenticated"]:
    app.show_consumption_page()
else:
    app.check_auth()
