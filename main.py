import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import gspread
from google.oauth2.service_account import Credentials

# Inicializar Flask
app = Flask(__name__)

# Configuración de OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Cargar credenciales de Google desde la variable de entorno
google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
if not google_creds_json:
    raise RuntimeError("Falta la variable de entorno GOOGLE_CREDS_JSON")

creds_info = json.loads(google_creds_json)
credentials = Credentials.from_service_account_info(creds_info)

# Autenticación con Google Sheets (usando gspread)
gc = gspread.authorize(credentials)

# Usar el ID de la hoja desde las variables de entorno
spreadsheet_id = os.getenv("SHEET_ID")
if not spreadsheet_id:
    raise RuntimeError("Falta la variable de entorno SHEET_ID")

worksheet = gc.open_by_key(spreadsheet_id).sheet1

# Leer números autorizados desde la hoja de cálculo
authorized_numbers = worksheet.col_values(1)  # Columna A

@app.route("/", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender_number = request.values.get("From", "").replace("whatsapp:", "")

    resp = MessagingResponse()

    if sender_number not in authorized_numbers:
        resp.message("❌ Tu número no está autorizado para usar este servicio.")
        return str(resp)

    # Llamada a la API de GPT-4
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Ocurrió un error consultando GPT-4: {e}"

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
