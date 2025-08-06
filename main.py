
import os
import openai
import json
from flask import Flask, request
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Guardar archivo credentials.json
credentials_path = "credentials.json"
with open(credentials_path, "w") as f:
    f.write(os.environ["GOOGLE_CREDS_JSON"])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo
spreadsheet = client.open("Usuarios autorizados")
sheet = spreadsheet.worksheet("Hoja 1")

@app.route("/", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    # Validar número
    autorizado = False
    for row in sheet.get_all_values():
        if row[1] in sender:
            autorizado = True
            break

    if not autorizado:
        return "Tu número no está autorizado para usar este servicio."

    # Consultar GPT
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}],
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Hubo un error al consultar GPT-4: {e}"

    return reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
