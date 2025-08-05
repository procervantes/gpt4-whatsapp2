
import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("No entendí tu mensaje. ¿Puedes repetirlo?")
        return str(resp)

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Responde de manera clara y educativa como asistente académico."},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=300
        )
        reply = completion.choices[0].message["content"]
    except Exception as e:
        reply = f"Ocurrió un error al procesar tu mensaje. Intenta más tarde. ({str(e)})"

    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
