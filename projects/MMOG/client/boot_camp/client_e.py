#!/usr/bin/env python
# -*- coding: latin-1 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../../lib/')
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
        befehl = input("Befehl? (z.B.: help|status|spawn|harakiri|move#x,y)", False)  # False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben

        if befehl in (None,":bye"):
            break  # while Schleife verlassen

        elif befehl == "a":
            spawnen(game_client)

        elif befehl == "b":
            spawnen_x_mal(game_client, 10) # 10 x nacheinander spawnen

        elif befehl == "c":
            einen_schritt_nach_norden(game_client)

        elif befehl == "d":
            n_schritte_nach_norden(game_client, 3)

        # Verzweigung für einen_sicheren_schritt_nach_norden() einbauen

        else:
            game_client.publish(befehl)

        game_client.print_attribute()

def einen_sicheren_schritt_nach_norden(game_client):
    """
    Als fünfte Aufgabe bewegen Sie Ihre Figur einen Schritt nach Norden - OHNE von der Spielfläche zu fallen.

    Ändern Sie auch n_schritte_nach_norden(), diese neue, sichere Funktion zu verwenden.

    """

    # Auslesen der aktuellen Position aus den Attributen
    attribute = game_client.attribute()
    x_aktuell = attribute["position"][0]
    y_aktuell = attribute["position"][1]

    # Berechnung der Zielkoordinaten
    x_neu, y_neu = nord(x_aktuell, y_aktuell)

    # und absetzen des entsprechenden move#x,y Befehls
    # aber nur, wenn x_neu und y_neu nicht None
    # HIER VERBESSERN
    befehl = "move#{},{}".format(x_neu, y_neu)
    game_client.publish(befehl)


def n_schritte_nach_norden(game_client, n):
    """
    Als vierte Aufgabe bewegen Sie Ihre Figur n Schritte nach Norden.
    """

    for _ in range(n):
        einen_schritt_nach_norden(game_client)


def einen_schritt_nach_norden(game_client):
    """
    Als dritte Aufgabe bewegen Sie Ihre Figur einen Schritt nach Norden.

    Die aus ../../lib/moves.py importiere Bibliotheksfunktion nord() berechnet die Zielkoordinaten der Zelle nördlich der aktuellen Position.

    x_neu, y_neu = nord(x_aktuell, y_aktuell)

    """

    # Auslesen der aktuellen Position aus den Attributen
    attribute = game_client.attribute()
    x_aktuell = attribute["position"][0]
    y_aktuell = attribute["position"][1]

    # Berechnung der Zielkoordinaten
    x_neu, y_neu = nord(x_aktuell, y_aktuell)

    # und absetzen des entsprechenden move#x,y Befehls
    befehl = "move#{},{}".format(x_neu, y_neu)
    game_client.publish(befehl)


def spawnen_x_mal(game_client, n):
    """
    Als zweite Aufgabe spawnen Sie n mal nacheinander.
    """
    for _ in range(n):
        spawnen(game_client)


def spawnen(game_client):
    """
    Als erste Aufgabe spawnen Sie 1x.
    """
    befehl = "spawn"
    game_client.publish(befehl)

##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
