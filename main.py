from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").lower()
    print(f"Mensaje recibido: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()
    msg.body("Hola, soy tu asistente GPT-4 en WhatsApp 😊")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
