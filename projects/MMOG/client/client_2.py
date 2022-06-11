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
        
        print("Befehl: {}".format(nachricht))
        game_client.publish(nachricht)
        print_status(game_client)


def move_north(game_client):
    """
    Als dritte Aufgabe bewegen wir uns einen Schritt nach Norden.
    
    Fast Pass: nutzen Sie die Bibliotheksfunktion nord(x, y), welche ihnen die Zielkoordinaten vom aktuellen x und y-Wert aus berechnet.
    """
    attribute = game_client.attribute()
    x_aktuell = attribute["position"][0]
    y_aktuell = attribute["position"][1]
    
    pass


def move_north_n_steps(game_client, n=10):
    """
    Als vierte Aufgabe: n Schritte (default 10x) nach Norden.
    """

    pass


##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()