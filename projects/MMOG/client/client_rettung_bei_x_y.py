#!/usr/bin/env python
# -*- coding: latin-1 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../lib/')

# grundlegende Funktionen für die MQTT-Kommunikation mit dem Server
from game_client_lib import *

# vordefinierte Funktionen wie nord(), sued(), etc. ... zum Bewegen der Figur
from moves import *

# in client_lib.py liegen eigene "fertige" Funktionen, die man immer wieder bei den verschiedenen Spielen verwendet
from client_lib import *

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
        befehl = input("Befehl? (z.B.: help|status|spawn|harakiri|move#x,y)", False)  # False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben

        if befehl in (None,":bye"):
            break  # while Schleife verlassen

        # Verzweigung für rettung_bei_x_y() einbauen
        
        else:
            print("Befehl: {}".format(befehl))
            game_client.publish(befehl)

        print_status(game_client)


def rettung_bei_x_y(game_client, x_ziel = 0, y_ziel = 0):
    """
    Die Figur beweg sich so schnell wie möglich zu den Zielkoordinaten (default 0,0).

    """
    x_aktuell, y_aktuell = None, None
    while not (x_aktuell == x_ziel and y_aktuell == y_ziel):
        attribute = game_client.attribute()
        x_aktuell = attribute["position"][0]
        y_aktuell = attribute["position"][1]
        break # hier Ihren Algorithmus einbauen ...

##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
