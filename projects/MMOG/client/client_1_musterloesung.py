#!/usr/bin/env python
# -*- coding: latin-1 -*-
# -*- coding: utf-8 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../lib/')
from game_client_lib import *

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
        
        elif nachricht == "s1":
            spawnen(game_client)
        
        elif nachricht == "s10":
            spawnen_x_mal(game_client, 100)

        else:
            print("Befehl: {}".format(nachricht))
            game_client.publish(nachricht)
        
        print_status(game_client)


def spawnen(game_client):
    """
    Als erste Aufgabe spawnen wir 1x.
    """
    game_client.publish("spawn")


def spawnen_x_mal(game_client, n):
    """
    Als zweite Aufgabe spawnen wir 10x nacheinander.
    """
    for _ in range(n):
        spawnen(game_client)


##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()