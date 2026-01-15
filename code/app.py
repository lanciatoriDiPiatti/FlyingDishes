from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "messaggio": "Benvenuto a Flying Dishes API",
        "endpoint": "/calcola-media",
        "metodo": "POST",
        "esempio": {"numeri": [1, 2, 3, 4, 5]}
    })

@app.route('/calcola-media', methods=['POST'])
def calcola_media():
    try:
        dati = request.get_json()
        
        if not dati or 'numeri' not in dati:
            return jsonify({"errore": "Fornisci un JSON con chiave 'numeri'"}), 400
        
        numeri = dati['numeri']
        
        if not isinstance(numeri, list) or len(numeri) == 0:
            return jsonify({"errore": "La lista dei numeri non può essere vuota"}), 400
        
        # Converti tutti i numeri a float
        numeri = [float(n) for n in numeri]
        
        media = sum(numeri) / len(numeri)
        
        return jsonify({
            "numeri": numeri,
            "media": media,
            "quantita": len(numeri)
        })
    
    except ValueError as e:
        return jsonify({"errore": "Uno o più valori non sono numeri validi"}), 400
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
