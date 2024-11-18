import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

def load_csv(file):
    return pd.read_csv(file)

def load_google_sheet(sheet_url):
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)
    return pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
