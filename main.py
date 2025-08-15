import os
import json
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request, jsonify

# --- CONFIGURACIÓN ---
google_creds_json = os.environ.get("GOOGLE_CREDS_JSON")
if not google_creds_json:
    raise ValueError("No se encontró la variable de entorno 'GOOGLE_CREDS_JSON'.")

creds_info = json.loads(google_creds_json)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = Credentials.from_service_account_info(creds_info, scopes=SCOPES)

gc = gspread.authorize(credentials)

SHEET_ID = os.environ.get("SHEET_ID")
if not SHEET_ID:
    raise ValueError("No se encontró la variable de entorno 'SHEET_ID'.")

sheet = gc.open_by_key(SHEET_ID).sheet1

# --- FLASK APP ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor activo ✅"

@app.route("/leer", methods=["GET"])
def leer_datos():
    try:
        data = sheet.get_all_records()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/agregar", methods=["POST"])
def agregar_datos():
    try:
        new_data = request.json
        if not new_data:
            return jsonify({"status": "error", "message": "No se recibió JSON"}), 400
        values = [new_data[col] for col in new_data]
        sheet.append_row(values)
        return jsonify({"status": "success", "message": "Fila agregada"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
