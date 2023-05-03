
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive'
          ]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES,
)

SHEET_TITLE = st.secrets["gsheets"]["sheet_title"]

gc = gspread.authorize(credentials)
sh = gc.open(SHEET_TITLE)


class IndexSheet:

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        try:
            self.sheet = sh.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            print("Worksheet not found")
            raise Exception("Worksheet not found")

    def get_content_as_df(self):
        return pd.DataFrame(self.sheet.get_all_records())

    def add_row_to_sheet(self, body: list):
        self.sheet.append_row(body)

    def get_last_row(self):
        return self.sheet.get_all_records()[-1]

