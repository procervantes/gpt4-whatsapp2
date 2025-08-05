import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    if not incoming_msg:
        return str(MessagingResponse())

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Responde como asistente educativo para estudiantes universitarios."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Hubo un error al consultar GPT-4: {e}"

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(answer)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
