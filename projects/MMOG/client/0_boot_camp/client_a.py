#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../../lib/')
from game_client_lib import *

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
        befehl = input("Befehl? (z.B.: help|status|spawn|harakiri|move#x,y)", False)  # TigerJython: False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben
        #befehl = input("Befehl? (z.B.: help|status|spawn|harakiri|move#x,y)\n")  # Thonny Editor

        if befehl in (None,":bye"):
            break  # while Schleife verlassen

        elif befehl == "a":
            spawnen(game_client)

        else:
            game_client.publish(befehl)

        game_client.print_attribute()


def spawnen(game_client):
    """
    Als erste Aufgabe spawnen Sie 1x.
    """
    pass # pass löschen und den "spawn" Befehl via game_client publishen

##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
