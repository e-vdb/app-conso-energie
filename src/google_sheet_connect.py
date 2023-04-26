#import library
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


#gc = gspread.service_account(filename="creds.json")
#connect to the service account
gc = gspread.authorize(credentials)
#connect to your sheet (between "" = the name of your G Sheet, keep it short)
sh = gc.open("2023_01_01_emeline_pressoir")


def get_df_from_sheet():
    # Read a worksheet and create it if it doesn't exist
    worksheet_title = "2022_11_16_emeline_pressoir"
    #worksheet_title = "Feuille 1"
    try:
        worksheet = sh.worksheet(worksheet_title)
        return pd.DataFrame(worksheet.get_all_records())
    except gspread.WorksheetNotFound:
        print("Worksheet not found")
        return None
