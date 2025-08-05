import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client

# Cargar variables de entorno
load_dotenv()

# Leer variables desde .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Inicializar cliente de Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Crear app Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Servidor funcionando correctamente."

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    to_number = data.get("to")
    message_body = data.get("message")

    if not to_number or not message_body:
        return {"error": "Faltan parámetros 'to' o 'message'"}, 400

    message = client.messages.create(
        from_=TWILIO_PHONE_NUMBER,
        to=to_number,
        body=message_body
    )

    return {"status": "enviado", "sid": message.sid}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
