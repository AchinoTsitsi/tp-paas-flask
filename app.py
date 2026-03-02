from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Existing routes ---
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
        return jsonify({"error": "Aucune donnée JSON reçue"}), 400
    return jsonify({"received": data})

# --- Form route without templates folder ---
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nom = request.form.get('nom')
        classe = request.form.get('classe')
        return jsonify({"received": {"nom": nom, "classe": classe}})
    
    # HTML served directly as string
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Formulaire Étudiant</title>
    </head>
    <body>
        <h1>Formulaire Étudiant</h1>
        <form method="post">
            Nom: <input type="text" name="nom" required><br><br>
            Classe: <input type="text" name="classe" required><br><br>
            <input type="submit" value="Envoyer">
        </form>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
