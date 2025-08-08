import os
import json
from google.oauth2.service_account import Credentials
import gspread

# Cargar las credenciales de Google desde la variable de entorno
google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
if not google_creds_json:
    raise RuntimeError("Falta la variable de entorno GOOGLE_CREDS_JSON")

creds_info = json.loads(google_creds_json)
credentials = Credentials.from_service_account_info(creds_info)

# Autenticación con Google Sheets (usando gspread)
gc = gspread.authorize(credentials)
spreadsheet_id = os.getenv("SHEET_ID")  # ID de la hoja de Google
worksheet = gc.open_by_key(spreadsheet_id).sheet1
