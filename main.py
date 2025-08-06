
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Inicializa Flask
app = Flask(__name__)

# Inicializa OpenAI
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Autenticación con Google Sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client_sheet = gspread.authorize(creds)
sheet = client_sheet.open("Usuarios autorizados").sheet1

# Ruta principal
@app.route("/", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '').replace("whatsapp:", "")

    # Verifica si el número está autorizado
    numbers = sheet.col_values(1)
    if from_number not in numbers:
        return str(MessagingResponse().message("No estás autorizado para usar este servicio."))

    # Consulta a GPT-4
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Hubo un error al consultar GPT-4: {e}"

    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)

# Ejecutar
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    