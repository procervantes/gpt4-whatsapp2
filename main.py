from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Configura la API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # Llamada a GPT-4
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}],
            temperature=0.7
        )
        gpt_reply = response.choices[0].message.content.strip()
        msg.body(gpt_reply)
    except Exception as e:
        msg.body(f"Hubo un error al consultar GPT-4:\n\n{str(e)}")

    return str(resp)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
