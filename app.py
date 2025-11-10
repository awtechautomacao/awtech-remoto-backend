from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import os

app = Flask(__name__)
CORS(app)

REDIS_URL = "rediss://red-d48tjmn5r7bs738r61p0:pOnjCrQANSkjZxfv761DPj5UNxkOgDmc@ohio-keyvalue.render.com:6379"

r = redis.from_url(
    REDIS_URL,
    decode_responses=True,
    ssl=True
)

KEY = "perfis_awtech"

def load_profiles():
    data = r.get(KEY)
    if data:
        return json.loads(data)
    return []

def save_profiles(profiles):
    r.set(KEY, json.dumps(profiles))

@app.route("/perfis", methods=["GET"])
def listar():
    return jsonify(load_profiles())

@app.route("/perfis", methods=["POST"])
def salvar():
    profiles = load_profiles()
    new = request.json
    for p in profiles:
        if p["nome"] == new["nome"]:
            return jsonify({"error": "Perfil já existe"}), 400
    profiles.append(new)
    save_profiles(profiles)
    return jsonify({"status": "ok"})

@app.route("/perfis/<nome>", methods=["DELETE"])
def excluir(nome):
    profiles = load_profiles()
    new_list = [p for p in profiles if p["nome"] != nome]
    if len(new_list) == len(profiles):
        return jsonify({"error": "Perfil não encontrado"}), 404
    save_profiles(new_list)
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return "API Awtech Remoto - OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
