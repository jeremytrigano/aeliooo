#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Application avec interface Qt pour les Cuisine
    ======================
 
    Exécuter pour commencer la gestion des commandes en cuisine.
 
 
"""

import sys
from PySide2.QtWidgets import (
    QApplication, QTableWidget, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
import requests
import json
import sys
import re

# adresse du serveur flask
baseurl = 'http://localhost:5000/'


class wCuisine(QWidget):
    def __init__(self):
        super(wCuisine, self).__init__()
        self.layoutV = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setColumnCount(3)

        self.creationForm()
        self.layoutV.addWidget(self.tableWidget)
        self.setLayout(self.layoutV)

    def creationForm(self):
        self.tableWidget.clear()

        r = requests.get(baseurl + 'commandes/cuisine')

        dictCmd = json.loads(r.text)
        listCmd = dictCmd['commandes']

        self.tableWidget.setRowCount(len(listCmd))
        cpt = 0
        for cmd in listCmd:
            self.cmdName = QLabel(f"Commande numéro {cmd['id']}")
            if cmd['etat'] == 1:
                self.buttonEprep = QPushButton("À préparer")
                self.buttonEprep.setProperty(
                    'cmdId', f"pushButton_e{cmd['id']}")
            else:
                self.buttonEprep = QPushButton("En préparation")
                self.buttonEprep.setProperty(
                    'cmdId', f"pushButton_ce{cmd['id']}")
            self.buttonPrep = QPushButton("Préparée")
            self.buttonPrep.setProperty('cmdId', f"pushButton_p{cmd['id']}")

            self.buttonEprep.clicked.connect(self.ePrep)
            self.buttonPrep.clicked.connect(self.ePrep)

            self.tableWidget.setCellWidget(cpt, 0, self.cmdName)
            self.tableWidget.setCellWidget(cpt, 1, self.buttonEprep)
            self.tableWidget.setCellWidget(cpt, 2, self.buttonPrep)

            cpt += 1

    # actions liées au clic de boutons
    def ePrep(self):
        pb = self.sender()
        cmdIdProp = pb.property('cmdId')
        cmdId = re.findall("[0-9]{1,}$", cmdIdProp)
        if len(cmdId) > 0:
            cmdId = cmdId[0]
        else:
            cmdId = 0
        # si le bouton cliqué est "À préparer"
        if re.match("^pushButton_e", cmdIdProp):
            print("pushButton_e")
            pb.setProperty('cmdId', f"pushButton_ce{cmdId}")
            # modification bdd état commande à 2 En cours de préparation
            self.putReq(cmdId, 2)
            pb.setText('En préparation')
        # si le bouton cliqué est "Préparée"
        elif re.match("^pushButton_p", cmdIdProp):
            print("pushButton_p")
            pb.setProperty('cmdId', f"pushButton_cp{cmdId}")
            # modification bdd état commande à 3 Prêt
            self.putReq(cmdId, 3)
            pb.setText('Terminée')
        # recréation du table widget
        print("creationForm")
        self.creationForm()

    # requete http PUT
    def putReq(self, idc, etat):
        requests.put(baseurl + 'commandes', json={"id": idc, "etat": etat})


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mces = wCuisine()
    mces.show()

    sys.exit(app.exec_())
