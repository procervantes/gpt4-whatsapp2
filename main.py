import os
from flask import Flask, request
from openai import OpenAI
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Mensaje recibido: {incoming_msg}")

    reply = MessagingResponse()
    msg = reply.message()

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        response_text = completion.choices[0].message.content.strip()
        msg.body(response_text)
    except Exception as e:
        msg.body(f"Hubo un error al consultar GPT-4: {str(e)}")

    return str(reply)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)