import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World from Render Etudiant!"

@app.route('/api/data')
def data():
    return jsonify({"message": "Exemple de JSON via un PaaS"})

@app.route('/api/postdata', methods=['POST'])
def post_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    return jsonify({"received": data}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
