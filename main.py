import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import gspread
from google.oauth2.service_account import Credentials

# =======================
# CONFIGURACIÓN
# =======================

# Twilio
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
RECEIVER_PHONE_NUMBER = os.environ.get("RECEIVER_PHONE_NUMBER")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Google Sheets
SHEET_ID = os.environ.get("SHEET_ID")
google_creds_json = os.environ.get("GOOGLE_CREDS_JSON")
if not google_creds_json:
    raise ValueError("La variable GOOGLE_CREDS_JSON no está configurada.")

creds_info = json.loads(google_creds_json)
credentials = Credentials.from_service_account_info(creds_info)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(SHEET_ID).sheet1  # Hoja 1

# Flask App
app = Flask(__name__)

# =======================
# FUNCIONES
# =======================

def es_usuario_autorizado(numero):
    """Verifica si el número está en Google Sheets."""
    usuarios = sheet.col_values(1)  # Columna A: números autorizados
    return numero in usuarios

def obtener_respuesta_gpt(prompt):
    """Llama a la API de OpenAI GPT-4."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Hubo un error al consultar GPT-4: {e}"

# =======================
# RUTAS
# =======================

@app.route("/", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")
    
    resp = MessagingResponse()
    msg = resp.message()
    
    if not es_usuario_autorizado(from_number):
        msg.body("Lo siento, tu número no está autorizado para usar este servicio.")
        return str(resp)
    
    if incoming_msg == "":
        msg.body("No recibí ningún mensaje. Por favor escribe tu consulta.")
        return str(resp)
    
    # Genera la respuesta de GPT-4
    respuesta = obtener_respuesta_gpt(incoming_msg)
    msg.body(respuesta)
    
    return str(resp)

# =======================
# MAIN
# =======================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
