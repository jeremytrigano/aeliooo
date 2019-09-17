#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Serveur Flask Aeliooo
    ======================
 
    Exécuter pour gérer l'API Aeliooo.
 
 
"""

from flask import Flask, request, redirect, url_for, g, jsonify
from flask_cors import CORS, cross_origin
import sqlite3
import json


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app, support_credentials=True)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    sql = sqlite3.connect('cestlabase.db')
    sql.row_factory = dict_factory
    return sql


@app.route('/')
def index():
    return redirect(url_for('commandes'))


@app.route('/commandes', methods=['GET', 'POST', 'PUT'])
@cross_origin(supports_credentials=True)
def commandes():
    # Le client récupère ses commandes:
    # Requête GET @/commandes?nomClient=Baratoux
    if request.method == 'GET':
        if request.args.get('nomClient'):
            nomClient = request.args.get('nomClient')
            db = get_db()
            cmd_cur = db.execute(
                f"SELECT * FROM commandes WHERE nom = '{nomClient}'")
            rescmd = cmd_cur.fetchall()
            # Réponse JSON {'commandes': [{'id': 12, 'etat': 4}, ...]}
            return jsonify({'commandes': rescmd})
        else:
            return {'status': 'aucun client'}
    # Le client passe une commandes:
    # Requête POST @/commandes
    elif request.method == 'POST':
        # réception JSON {'nom': 'Baratoux', 'adresse': 'Rue machin', 'contenu': {}}
        res = request.get_json()
        res = res[0]
        nom = res['nom']
        adresse = res['adresse']
        db = get_db().cursor()
        db.execute(
            f"INSERT INTO commandes(nom, adresse) values('{nom}', '{adresse}')")
        get_db().commit()
        # Réponse JSON {'retour': ’OK’}
        return {'retour': 'OK'}
    # La cuisine met la commande à jour:
    # Le livreur met la commande à jour:
    # Requête PUT @/commandes
    elif request.method == 'PUT':
        res = request.get_json()
        if isinstance(res, list):
            res = res[0]
        idc = res['id']
        etat = res['etat']
        db = get_db()
        db.execute(
            f" UPDATE commandes SET etat='{etat}' WHERE id='{idc}'")
        db.commit()
        # Réponse JSON {'id': 12, 'etat': 3}
        return {'id': idc, 'etat': etat}
    else:
        return "Bienvenue chez Aeliooo - Les commandes "


# La cuisine récupère ses commandes:
# Requête GET @/commandes/cuisine
@app.route('/commandes/cuisine')
def commandesCuisine():
    db = get_db()
    cmd_cur = db.execute('SELECT * FROM commandes WHERE etat BETWEEN 1 AND 2')
    rescmd = cmd_cur.fetchall()
    # Réponse JSON {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4, 'contenu': {....}}, ...]}
    # return {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4, 'contenu': {}}, {'id': 13, 'nom': 'Ludo', 'etat': 4, 'contenu': {}}]}
    return jsonify({'commandes': rescmd})

# Le livreur récupère ses livraisons:
# Requête GET @/commandes/livreur
@app.route('/commandes/livreur')
def commandesLivreur():
    db = get_db()
    cmd_cur = db.execute('SELECT * FROM commandes WHERE etat BETWEEN 3 AND 4')
    rescmd = cmd_cur.fetchall()
    # Réponse JSON {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4}, ...]}
    # return {'commandes': [{'id': 12, 'nom': 'Baratoux', 'etat': 4}]}
    return jsonify({'commandes': rescmd})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
