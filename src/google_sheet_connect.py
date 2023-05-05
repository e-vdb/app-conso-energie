"""Module for connecting to Google Sheets and adding data to it."""

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

from src.exceptions import WorksheetError

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES,
)

SHEET_TITLE = st.secrets["gsheets"]["sheet_title"]

gc = gspread.authorize(credentials)
sh = gc.open(SHEET_TITLE)


class IndexSheet:
    """Class to manage the sheet with consumption indexes."""

    def __init__(self, sheet_name):
        """
        Initialize the class.

        Parameters
        ----------
        sheet_name: str
            The name of the sheet.

        Raises
        ------
        Exception: If the sheet is not found.
        """
        self.sheet_name = sheet_name
        try:
            self.sheet = sh.worksheet(sheet_name)
        except gspread.WorksheetNotFound as exc:
            raise WorksheetError(f"Worksheet {sheet_name} not found.") from exc

    def get_content_as_df(self):
        """Return the content of the sheet as a dataframe."""
        return pd.DataFrame(self.sheet.get_all_records())

    def add_row_to_sheet(self, body: list):
        """Add a row to the sheet."""
        self.sheet.append_row(body)

    def get_last_row(self) -> dict:
        """Return the last row of the sheet."""
        return self.sheet.get_all_records()[-1]
