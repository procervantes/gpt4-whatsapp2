import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def check():
    return 'Servidor activo ✅'

@app.route('/', methods=['POST'])
def reply_whatsapp():
    # Leer el mensaje entrante
    incoming_msg = request.values.get('Body', '').lower()

    # Crear la respuesta
    resp = MessagingResponse()
    msg = resp.message()

    # Lógica de respuesta
    if 'hola' in incoming_msg:
        msg.body('¡Hola! Soy Lucy 🤖 ¿En qué te puedo ayudar hoy?')
    else:
        msg.body(f'No entendí tu mensaje: "{incoming_msg}". Intenta decir "hola".')

    return str(resp)

if __name__ == '__main__':
    app.run()
