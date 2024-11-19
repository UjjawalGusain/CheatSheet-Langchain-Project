import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import gspread
import os
import json
from dotenv import load_dotenv
from dashboard import st

load_dotenv()

# if "GOOGLE_SHEET_CREDENTIALS" not in os.environ:
#     os.environ["GOOGLE_SHEET_CREDENTIALS"] = os.getenv("GOOGLE_SHEET_CREDENTIALS")


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
credentials_json = st.secrets["GOOGLE_SHEET_CREDENTIALS"]

# Parse the JSON and use it to authenticate
credentials_info = json.loads(credentials_json)
creds = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
client = gspread.authorize(creds)

def load_csv(file):
    return pd.read_csv(file)

def load_google_sheet(sheet_url):
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)
    return pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
