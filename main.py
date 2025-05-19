
import webbrowser
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔐 Reemplazá esto con tu clave real de OpenAI
client = OpenAI(api_key="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")

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
        return jsonify({ "reply": f"Hubo un error al consultar la IA: {str(e)}" })

def abrir_navegador():
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    threading.Timer(1, abrir_navegador).start()
    app.run(debug=False)
