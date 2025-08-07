# GPT-4 WhatsApp con control por Google Sheets

Este proyecto permite conectar WhatsApp con GPT-4 y controlar el acceso mediante un documento de Google Sheets.

### Variables de entorno necesarias en Render

- `OPENAI_API_KEY` – Tu clave de OpenAI.
- `GOOGLE_CREDS_JSON` – El contenido del JSON de credenciales (una sola línea).
- `SHEET_ID` – ID del Google Sheet.

### Requisitos

- La hoja debe compartirse con el service account como editor.
- El ID de la hoja se obtiene de la URL: `https://docs.google.com/spreadsheets/d/{ID}/edit#gid=0`.