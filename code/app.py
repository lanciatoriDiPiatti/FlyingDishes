from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok"})

@app.route('/calcola-media', methods=['POST'])
def calcola_media():
    try:
        numeri = request.get_json().get('numeri', [])
        if not numeri:
            return jsonify({"errore": "Fornisci lista 'numeri'"}), 400
        media = sum(numeri) / len(numeri)
        return jsonify({"media": media})
    except Exception as e:
        return jsonify({"errore": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
