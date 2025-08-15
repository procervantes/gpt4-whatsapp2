import os
import gspread
from google.oauth2.service_account import Credentials
import json

# Cargar credenciales
google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
creds_info = json.loads(google_creds_json)
credentials = Credentials.from_service_account_info(creds_info)

# Conectar con Google Sheets usando SHEET_ID
gc = gspread.authorize(credentials)
spreadsheet_id = os.getenv("SHEET_ID")
worksheet = gc.open_by_key(spreadsheet_id).sheet1
