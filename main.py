
import os
import webbrowser
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔐 Reemplazá esto con tu API Key real de OpenAI
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Sos un asistente de ventas de Casa del Audio. Respondé de forma útil y clara sobre productos, ofertas, sucursales y servicios."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({ "reply": reply })
    except Exception as e:
        return jsonify({ "reply": f"Error del servidor: {str(e)}" })

# Configurar el puerto según Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
