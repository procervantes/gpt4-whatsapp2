
import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import gspread

# Crear archivo temporal con las credenciales de Google
credentials_path = "credentials.json"
with open(credentials_path, "w") as f:
   

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Inicializar gspread
gc = gspread.service_account(filename=credentials_path)
sheet = gc.open("Usuarios autorizados").worksheet("Hoja 1")

# Leer números autorizados
autorizados = sheet.col_values(1)

# Inicializar OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Inicializar Flask
app = Flask(__name__)

@app.route("/", methods=["POST"])
def whatsapp_reply():
    numero = request.form.get("From", "")
    mensaje = request.form.get("Body", "").strip()

    respuesta = MessagingResponse()

    if numero not in autorizados:
        respuesta.message("❌ Este número no está autorizado para usar este servicio.")
    else:
        try:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": mensaje}]
            )
            respuesta.message(completion.choices[0].message.content)
        except Exception as e:
            respuesta.message(f"⚠️ Error al consultar GPT-4: {e}")

    return str(respuesta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
