import os
import json
import openai
import gspread
from flask import Flask, request
from google.oauth2.service_account import Credentials

# Inicializar Flask
app = Flask(__name__)

# Configurar OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Configurar Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]
GOOGLE_CREDS_JSON = os.environ.get("GOOGLE_CREDS_JSON")
SPREADSHEET_ID = os.environ.get("SHEET_ID")

if not GOOGLE_CREDS_JSON or not SPREADSHEET_ID:
    raise RuntimeError("Faltan variables de entorno necesarias.")

creds_info = json.loads(GOOGLE_CREDS_JSON)
credentials = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1

# Endpoint raíz
@app.route("/", methods=["GET"])
def home():
    return "Servidor activo ✅"

# Endpoint de prueba
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    # Leer usuarios autorizados desde Google Sheets
    usuarios = worksheet.col_values(1)  # Columna A: Números autorizados

    if sender not in usuarios:
        return "Número no autorizado."

    # Llamada a OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": incoming_msg}]
    )
    reply = response["choices"][0]["message"]["content"]
    return reply

if __name__ == "__main__":
    app.run(debug=True)