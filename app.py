from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import redis
import ssl
import os

app = Flask(__name__)
CORS(app)

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise Exception("A variável REDIS_URL não foi definida no Render!")

r = redis.Redis.from_url(
    REDIS_URL,
    ssl_cert_reqs=ssl.CERT_NONE
)

KEY = "profiles"

def load_profiles():
    try:
        data = r.get(KEY)
        if not data:
            return []
        return json.loads(data)
    except Exception as e:
        print("Erro ao carregar perfis:", e)
        return []

def save_profiles(lista):
    try:
        r.set(KEY, json.dumps(lista))
    except Exception as e:
        print("Erro ao salvar perfis:", e)

@app.route("/")
def home():
    return jsonify({"status": "API ONLINE", "redis": True})

@app.route("/perfis", methods=["GET"])
def listar():
    return jsonify(load_profiles())

@app.route("/perfis", methods=["POST"])
def adicionar():
    novo = request.json
    lista = load_profiles()
    lista.append(novo)
    save_profiles(lista)
    return jsonify({"status": "salvo", "item": novo}), 201

@app.route("/perfis", methods=["DELETE"])
def limpar():
    r.delete(KEY)
    return jsonify({"status": "limpo"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
