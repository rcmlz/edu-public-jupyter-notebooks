#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################################################
# Imports
##############################################################
import sys
# Im lib-Ordner finden Sie ggf. interessante Funktionen, die Sie benutzen können (und die auch der Server nutzt).
sys.path.append('../lib/')
from game_client_lib import *
from moves import *

# Falls wir Funktionen auslagern wollen (und damit u.A. leichter testbar machen), können wir diese in Bibliotheks-Python-Dateien speichern,
# aus welchen wir wie gewohnt so die Funktionen importieren:
from client_gehirn_vorlage import *

##############################################################
# Settings
##############################################################
spieler = "some_player_name@somewhere.org"

game_client = Game_Client(spieler, "../config/config.json")

##############################################################
# Programm
##############################################################

while True:
    nachricht = input("Befehl? (z.B.: help)", False)  # False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben

    if nachricht in [None,":bye"]:
        break  # while Schleife verlassen

    elif nachricht == "a":
        attribute = game_client.attribute()
        print("Aktuelle Attribute: {}".format(attribute))

    elif nachricht == "r":
        rettung_bei_x_y(game_client)
    
    else:
        game_client.publish(nachricht)

game_client.disconnect()
