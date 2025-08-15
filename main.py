import os
import json
from google.oauth2.service_account import Credentials
import gspread
from openai import OpenAI
from twilio.rest import Client
from flask import Flask, request, jsonify

# Leer Google creds desde ENV
google_creds_json = os.environ.get("GOOGLE_CREDS_JSON")
if not google_creds_json:
    raise Exception("La variable de entorno GOOGLE_CREDS_JSON no está configurada")
creds_info = json.loads(google_creds_json)
credentials = Credentials.from_service_account_info(creds_info)

# Conectar a Google Sheets
SHEET_ID = os.environ.get("SHEET_ID")
if not SHEET_ID:
    raise Exception("La variable de entorno SHEET_ID no está configurada")
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(SHEET_ID).sheet1

# Configurar OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY no configurada")
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Configurar Twilio
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH = os.environ.get("TWILIO_AUTH")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
if not all([TWILIO_SID, TWILIO_AUTH, TWILIO_PHONE]):
    raise Exception("Credenciales de Twilio incompletas")
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Flask app
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_msg = data.get("message")
    phone = data.get("phone")
    if not user_msg or not phone:
        return jsonify({"error":"Faltan campos"}), 400

    # Lógica de GPT
    response = client_ai.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":user_msg}]
    )
    reply = response.choices[0].message.content

    # Enviar por Twilio
    twilio_client.messages.create(
        body=reply,
        from_=TWILIO_PHONE,
        to=phone
    )
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
