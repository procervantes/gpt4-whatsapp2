
import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Configurar OpenAI
openai.api_key = os.environ["OPENAI_API_KEY"]

# Autenticación con Google Sheets usando GOOGLE_CREDS_JSON
creds_json = json.loads(os.environ["GOOGLE_CREDS_JSON"])
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credentials = Credentials.from_service_account_info(creds_json, scopes=scopes)
gc = gspread.authorize(credentials)

# Abrir hoja de cálculo y worksheet
spreadsheet = gc.open("Usuarios autorizados")
worksheet = spreadsheet.sheet1

# Leer todos los números autorizados
numeros_autorizados = worksheet.col_values(1)  # asumiendo que la columna A tiene los teléfonos

@app.route("/", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    sender_number = request.values.get("From", "").replace("whatsapp:", "")

    resp = MessagingResponse()

    if sender_number not in numeros_autorizados:
        resp.message("⚠️ Acceso no autorizado.")
        return str(resp)

    # Si está autorizado, responde con GPT-4
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Hubo un error al consultar GPT-4: {e}"

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
