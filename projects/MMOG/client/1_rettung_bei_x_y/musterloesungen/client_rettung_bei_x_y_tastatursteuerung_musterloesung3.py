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
    
    #Referenz auf Funktionen nord(), nord_west() etc. in Woerterbuch speichern
    steuerung = {
             "d": nord
            ,"s": nord_west
            ,"f": nord_ost
            ,"x": sued
            ,"y": sued_west
            ,"c": sued_ost
    }
    
    while True:
        befehl = input("Befehl? (z.B.: a| {})".format(steuerung.keys()), False)  # TigerJython: False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben
        
        # aktueller Standort
        attribute = game_client.attribute()
        x_aktuell, y_aktuell = attribute["position"]
        
        if befehl in (None,":bye"):
            break  # while Schleife verlassen

        elif befehl == "a":
            befehl = "spawn"

        elif befehl in steuerung.keys():
            x_neu, y_neu = steuerung[befehl](x_aktuell, y_aktuell)
            befehl = "move#{},{}".format(x_neu, y_neu)

        else:
            print("Befehl {} nicht erkannt".format(befehl))
            continue # naechster Schleifendurchlauf

        game_client.publish(befehl)
        game_client.print_attribute()

##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
