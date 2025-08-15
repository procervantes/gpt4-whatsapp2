import os
import json
from google.oauth2.service_account import Credentials

# Leer la variable de entorno
google_creds_json = os.environ.get("GOOGLE_CREDS_JSON")

# Convertirla a dict
if not google_creds_json:
    raise ValueError("No se encuentra GOOGLE_CREDS_JSON en las variables de entorno")

creds_info = json.loads(google_creds_json)

# Crear credenciales de Google Sheets
credentials = Credentials.from_service_account_info(creds_info)
