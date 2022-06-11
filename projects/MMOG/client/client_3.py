#!/usr/bin/env python
# -*- coding: latin-1 -*-
# -*- coding: utf-8 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../lib/')
from game_client_lib import *
from moves import * # vordefinierte Funktionen zum Bewegen der Figur

##############################################################
# Einstellungen
##############################################################
spieler = "some_player_name@somewhere.org"

game_client = Game_Client(spieler, "../config/config.json")

##############################################################
# Funktionen
##############################################################

def manuelle_steuerung(game_client):
    """
    Sendet eingegebene Befehle zum Server und gibt des Status auf der Konsole aus.
    """
    while True:
        nachricht = input("Befehl? (z.B.: help|status|spawn|harakiri|move#x,y)", False)  # False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben

        if nachricht in (None,":bye"):
            break  # while Schleife verlassen

        elif nachricht == "r":
            rettung_bei_x_y(game_client, 0, 0)

        else:
            print("Befehl: {}".format(nachricht))
            game_client.publish(nachricht)

        print_status(game_client)


def rettung_bei_x_y(game_client, x_ziel = 0, y_ziel = 0):
    """
    Wir bewegen uns moeglichst schnell zu den Zielkoordinaten (default 0,0).

    Fast Pass: nutzen Sie die Bibliotheksfunktionen

    nord(x, y)
    sued(x, y)
    nord_west(x, y)
    sued_west(x, y)
    nord_ost(x, y)
    sued_ost(x, y)

    """
    x_aktuell, x_aktuell = None, None
    while not (x_aktuell == x_ziel and y_aktuell == y_ziel):
        attribute = game_client.attribute()
        x_aktuell = attribute["position"][0]
        y_aktuell = attribute["position"][1]
        break


##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
