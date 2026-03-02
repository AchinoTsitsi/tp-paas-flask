import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# --- Routes GET ---
@app.route('/')
def home():
    return "Hello World from Render Etudiant!"

@app.route('/api/data')
def data():
    return jsonify({"message": "Exemple de JSON via un PaaS"})

# --- Route POST ---
@app.route('/api/postdata', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Aucune donnée JSON reçue"}), 400
    return jsonify({"received": data})

# --- Formulaire HTML ---
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nom = request.form.get('nom')
        classe = request.form.get('classe')
        return jsonify({"received": {"nom": nom, "classe": classe}})
    return render_template('form.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)