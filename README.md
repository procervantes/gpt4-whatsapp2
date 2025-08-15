# GPT-4 WhatsApp App - Render Free

Esta app permite que alumnos de la universidad accedan a GPT-4 por WhatsApp usando Twilio.

## Configuración

1. Variables de entorno en Render:
   - OPENAI_API_KEY
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - TWILIO_PHONE_NUMBER
   - RECEIVER_PHONE_NUMBER
   - SHEET_ID
   - GOOGLE_CREDS_JSON (JSON de la cuenta de servicio de Google, **en una sola línea**)

2. Requirements:
   ```bash
   pip install -r requirements.txt
