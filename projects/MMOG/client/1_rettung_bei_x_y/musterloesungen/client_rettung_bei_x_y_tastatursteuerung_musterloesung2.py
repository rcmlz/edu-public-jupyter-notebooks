#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../../lib/')

# grundlegende Funktionen für die MQTT-Kommunikation mit dem Server
from game_client_lib import *

# vordefinierte Funktionen wie nord(), sued(), etc. ... zum Bewegen der Figur
from moves import *

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
        befehl = input("Befehl? (z.B.: a| s d f | y x c)", False)  # TigerJython: False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben
        
        # aktueller Standort
        attribute = game_client.attribute()
        x_aktuell, y_aktuell = attribute["position"]
        
        if befehl in (None,":bye"):
            break  # while Schleife verlassen
        
        elif befehl == "a":
            game_client.publish("spawn")
            continue # naechster Schleifendurchlauf

        elif befehl == "d":
            f = nord # Referenz auf Funktion nord() in f speichern
        
        elif befehl == "s":
            f = nord_west # Referenz auf Funktion nord_west() in f speichern
        
        elif befehl == "f":
            f = nord_ost
        
        elif befehl == "x":
            f = sued
        
        elif befehl == "y":
            f = sued_west
        
        elif befehl == "c":
            f = sued_ost
        
        else:
            print("Befehl {} nicht erkannt".format(befehl))
            continue # naechster Schleifendurchlauf

        x_neu, y_neu = f(x_aktuell, y_aktuell)
        befehl = "move#{},{}".format(x_neu, y_neu)
        game_client.publish(befehl)
        game_client.print_attribute()

##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
