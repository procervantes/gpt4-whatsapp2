import os
import json
from google.oauth2.service_account import Credentials
import gspread
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)

# Cargar credenciales de Google
google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
if not google_creds_json:
    raise RuntimeError("La variable de entorno GOOGLE_CREDS_JSON no está definida")

creds_info = json.loads(google_creds_json)
credentials = Credentials.from_service_account_info(creds_info)

gc = gspread.authorize(credentials)
spreadsheet_id = os.getenv("SHEET_ID")
worksheet = gc.open_by_key(spreadsheet_id).sheet1

# Configurar API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ejemplo básico de webhook de WhatsApp
@app.route("/", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender_number = request.values.get("From", "").replace("whatsapp:", "")
    resp = MessagingResponse()

    authorized_numbers = worksheet.col_values(1)
    if sender_number not in authorized_numbers:
        resp.message("❌ Tu número no está autorizado para usar este servicio.")
        return str(resp)

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
