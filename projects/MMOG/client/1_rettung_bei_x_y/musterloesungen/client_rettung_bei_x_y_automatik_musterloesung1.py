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

# in client_lib.py liegen eigene "fertige" Funktionen, die man immer wieder bei den verschiedenen Spielen verwendet
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

        elif befehl == "r":
            rettung_bei_x_y(game_client)

        else:
            game_client.publish(befehl)

        game_client.print_attribute()


def rettung_bei_x_y(game_client, x_ziel = 0, y_ziel = 0):
    """
    Die Figur bewegt sich so schnell wie moeglich zu den Zielkoordinaten (default 0,0).

    """
    # zunächst einmal die Attribute automatisch aktualisieren, damit wir wissen, wo wir stehen.
    game_client.publish("status")
    game_client.print_attribute()

    # aktuelle Standortkoordinaten in Variablen speichern
    attribute = game_client.attribute()
    x_aktuell, y_aktuell = attribute["position"]

    # Abbruchbedingungen
    ziel_erreicht = x_aktuell == x_ziel and y_aktuell == y_ziel
    hoffung = 10 # wenn auf 0 runtergezaehlt wurde (und wir feststecken), verlassen wir die Schleife. Die Zahl 0 entspricht auch False, alles ausser 0 entspricht auch True
    
    while not ziel_erreicht and hoffung:
    
        # nach nord_west
        x_neu, y_neu = nord_west(x_aktuell, y_aktuell)
        befehl = "move#{},{}".format(x_neu, y_neu)
        game_client.publish(befehl)
                
        # Standortkoordinaten nach Bewegung
        attribute = game_client.attribute()
        x_aktuell, y_aktuell = attribute["position"]

        # nach nord
        x_neu, y_neu = nord(x_aktuell, y_aktuell)
        befehl = "move#{},{}".format(x_neu, y_neu)
        game_client.publish(befehl)

        # Standortkoordinaten nach Bewegung
        attribute = game_client.attribute()
        x_aktuell, y_aktuell = attribute["position"]

        # nach sued_west
        x_neu, y_neu = sued_west(x_aktuell, y_aktuell)
        befehl = "move#{},{}".format(x_neu, y_neu)
        game_client.publish(befehl)
        
        # Standortkoordinaten nach Bewegung
        attribute = game_client.attribute()
        x_aktuell, y_aktuell = attribute["position"]

        # Abbruchbedingung aktualisieren
        ziel_erreicht = x_aktuell == x_ziel and y_aktuell == y_ziel
        hoffung -= 1


##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
