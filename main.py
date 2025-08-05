import os
from flask import Flask, request
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECEIVER_PHONE_NUMBER = os.getenv("RECEIVER_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/", methods=["GET"])
def index():
    return "Servidor funcionando"

@app.route("/", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").lower()
    sender = request.values.get("From", "")

    response = ""
    if "hola" in incoming_msg:
        response = "¡Hola! ¿En qué puedo ayudarte?"
    else:
        response = "Recibido: " + incoming_msg

    client.messages.create(
        body=response,
        from_=TWILIO_PHONE_NUMBER,
        to=sender
    )

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
