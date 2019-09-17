import sys
from PySide2.QtWidgets import QApplication, QTableWidget, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import requests
import json
import sys
import re

baseurl = 'http://localhost:5000/'


class wCuisine(QWidget):
    def __init__(self):
        super(wCuisine, self).__init__()
        self.layoutV = QVBoxLayout()
        self.tableWidget = QTableWidget()
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
            else:
                self.buttonEprep = QPushButton("En préparation")
            self.buttonEprep.setProperty('cmdId', f"pushButton_e{cmd['id']}")
            self.buttonPrep = QPushButton("Préparée")
            self.buttonPrep.setProperty('cmdId', f"pushButton_p{cmd['id']}")

            self.buttonEprep.clicked.connect(self.ePrep)
            self.buttonPrep.clicked.connect(self.ePrep)

            self.tableWidget.setCellWidget(cpt, 0, self.cmdName)
            self.tableWidget.setCellWidget(cpt, 1, self.buttonEprep)
            self.tableWidget.setCellWidget(cpt, 2, self.buttonPrep)

            cpt += 1

    def ePrep(self):
        pb = self.sender()
        cmdIdProp = pb.property('cmdId')
        cmdId = re.findall("[0-9]{1,}$", cmdIdProp)
        if len(cmdId) > 0:
            cmdId = cmdId[0]
        else:
            cmdId = 0
        if re.match("^pushButton_e", cmdIdProp):
            pb.setProperty('cmdId', f"pushButton_ce{cmdId}")
            self.putReq(cmdId, 2)
            pb.setText('En préparation')
        elif re.match("^pushButton_p", cmdIdProp):
            pb.setProperty('cmdId', f"pushButton_cp{cmdId}")
            self.putReq(cmdId, 3)
            pb.setText('Terminée')
        self.refresh()

    def refresh(self):
        self.creationForm()

    def putReq(self, idc, etat):
        requests.put(baseurl + 'commandes', json={"id": idc, "etat": etat})


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mces = wCuisine()
    mces.show()

    sys.exit(app.exec_())
