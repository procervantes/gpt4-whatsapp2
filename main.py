import os
from dotenv import load_dotenv

load_dotenv()  # Esto lee tu archivo .env y carga las variables

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '¡Hola desde Render!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

