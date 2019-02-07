# LoraServer

* Se créer un compte sur : https://lora.campusiot.imag.fr

* Ajouter une application avec le nom de votre projet

* Dans l'application, ajouter un device, ici nous utilisons un microchip RN2483. Générer un device EUI aléatoire. Device-profile : Classe A


# Connection Serial

* Installer pySerial : pip3 install pySerial

* Brancher l'usb serial sur un port usb

* Pour connaître le port serial, entrer dans votre terminal :
    python3 -m serial.tools.list_ports

* Modifier SERIAL_PORT par l'url du port serial obtenu précedement

# Paramétrer le module RN2483

* Modifier DEV_UI et APP_KEY selon les clefs générés sur LoraServer

* Pour les versions 1.0 de loraware, il n'est pas nécessaire d'avoir une APP_UI

# Tester

* Lancer test.py, des données devraient arriver sur votre serveur Lora.

# Erreurs possibles

* Vous êtes trop loin de l'antenne, ou des éléments interfèrent (se mettre dehors)

