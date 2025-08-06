import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from google.oauth2 import service_account
import gspread

# Escribir credenciales en un archivo temporal
credentials_path = "credentials.json"
with open(credentials_path, "w") as f:
    f.write(os.environ["GOOGLE_CREDS_JSON"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Autenticación con Google Sheets
creds = service_account.Credentials.from_service_account_file(credentials_path)
client = gspread.authorize(creds)
sheet = client.open("Usuarios autorizados").worksheet("Hoja 1")

# Verificar si el número está autorizado
def numero_autorizado(numero):
    numeros = sheet.col_values(1)
    return numero in numeros

# Inicializar Flask y OpenAI
app = Flask(__name__)
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "").replace("whatsapp:", "")

    resp = MessagingResponse()
    msg = resp.message()

    if not numero_autorizado(from_number):
        msg.body("Lo siento, tu número no está autorizado para usar este servicio.")
        return str(resp)

    if incoming_msg:
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": incoming_msg}]
            )
            respuesta = completion.choices[0].message.content
            msg.body(respuesta)
        except Exception as e:
            msg.body(f"Error al consultar GPT-4: {str(e)}")
    else:
        msg.body("Hola, soy tu asistente GPT-4 en WhatsApp 😊")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
