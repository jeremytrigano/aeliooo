from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Bienvenue chez Aeliooo"


@app.route('/commandes', methods=['GET', 'POST', 'PUT'])
def commandes():
    # Le client récupère ses commandes:
    # Requête GET @/commandes?nomClient=Baratoux
    if request.method == 'GET':
        if request.args.get('nomClient'):
            nomClient = request.args.get('nomClient')
            # select cmd str(nomClient)
            # Réponse JSON {'commandes': [{'id': 12, 'etat': 4}, ...]}
            return {'commandes': [{'id': 12, 'etat': 4}, {'id': 13, 'etat': 5}], 'nom': nomClient}
        else:
            return {'status': 'aucun client'}
    # Le client passe une commandes:
    # Requête POST @/commandes
    elif request.method == 'POST':
        # réception JSON {'nom': 'Baratoux', 'adresse': 'Rue machin', 'contenu': {}}
        # Réponse JSON {'retour': ’OK’}
        return {'retour': 'OK'}
    # La cuisine met la commande à jour:
    # Le livreur met la commande à jour: hghg
    # Requête PUT @/commandes
    elif request.method == 'PUT':
        # Réponse JSON {'id': 12, 'etat': 3}
        return {'id': 12, 'etat': 3}
    else:
        return "Bienvenue chez Aeliooo - Les commandes "


# La cuisine récupère ses commandes:
# Requête GET @/commandes/cuisine
@app.route('/commandes/cuisine')
def commandesCuisine():
    # Réponse JSON {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4, 'contenu': {....}}, ...]}
    return {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4, 'contenu': {}}]}

# Le livreur récupère ses livraisons:
# Requête GET @/commandes/livreur
@app.route('/commandes/livreur')
def commandesLivreur():
    # Réponse JSON {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4}, ...]}
    return {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4}]}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
