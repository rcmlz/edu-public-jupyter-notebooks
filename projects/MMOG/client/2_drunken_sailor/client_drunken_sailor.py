#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../')
sys.path.append('../../lib/')

# grundlegende Funktionen für die MQTT-Kommunikation mit dem Server
from game_client_lib import *

# vordefinierte Funktionen wie nord(), sued(), etc. ... zum Bewegen der Figur
from moves import *

# in client_lib.py  liegen eigene "fertige" Funktionen, die man immer wieder bei den verschiedenen Spielen verwendet
from client_lib import *

##############################################################
# Einstellungen
##############################################################
spieler = "some_player_name@somewhere.org"

game_client = Game_Client(spieler, "../../config/config.json")

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

        elif befehl == "d":
            drunken_sailor(game_client, 10)

        else:
            game_client.publish(befehl)

        game_client.print_attribute()


def drunken_sailor(game_client, n):
    """
    Die Figur bewegt sich so schnell wie moeglich zufaellig n Schritte, ohne von der Spielflaeche zu fallen.

    """
    x_aktuell, y_aktuell = None, None

    while True: # hier korrekte Bedingung anstelle von True einfuegen
        attribute = game_client.attribute()
        x_aktuell = attribute["position"][0]
        y_aktuell = attribute["position"][1]

        break # hier ihren Algorithmus einbauen

##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
