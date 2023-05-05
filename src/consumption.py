"""Class for consumption computation."""

import pandas as pd
from dateutil.relativedelta import relativedelta


class ConsumptionDataframe:
    """Class for consumption computation."""

    def __init__(self, df: pd.DataFrame):
        """Initialise the class."""
        self.df = df
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df.sort_values(by="date", inplace=True)
        self.consumption_columns: list = []
        zero_cols = [col for col in df.columns if (df[col] == 0).all()]
        self.saved_columns = [
            col for col in self.df.columns if col not in zero_cols
        ]

    def consumption(self, new_col: str, col_index: str):
        """Compute consumption for a given column."""
        self.df[new_col] = self.df[col_index].diff()
        self.df["consumption_month"] = (
            self.df["date"]
            .apply(lambda x: x - relativedelta(months=1))
            .dt.month_name()
        )

    def evaluate_consumption(self):
        """Compute consumption for each column."""
        for col in self.saved_columns:
            new_col = col + "_consumption"
            self.consumption_columns.append(new_col)
            self.df[new_col] = self.df[col].diff()

        self.df["Month_consumption"] = (
            self.df["date"]
            .apply(lambda x: x - relativedelta(months=1))
            .dt.month_name()
        )
        self.df["Year_consumption"] = (
            self.df["date"]
            .apply(lambda x: x - relativedelta(months=1))
            .dt.year
        )

    def set_index_date(self):
        """Set date as index."""
        self.df.set_index("date", inplace=True)

    def filter_year(self, year: str):
        """Filter dataframe by year."""
        filt = (self.df["date"] >= year + "-02-01") & (
            self.df["date"] < f"{str(int(year) + 1)}-02-01"
        )
        return self.df.loc[filt]
