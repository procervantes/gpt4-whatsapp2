import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECEIVER_PHONE_NUMBER = os.getenv("RECEIVER_PHONE_NUMBER")

@app.route("/", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    if incoming_msg:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        answer = response.choices[0].message["content"].strip()
    else:
        answer = "Hola, soy tu asistente GPT-4 en WhatsApp 😊"

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(answer)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)