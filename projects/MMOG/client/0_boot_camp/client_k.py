#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################
# Imports
##############################################################
import sys
sys.path.append('../../lib/')
from game_client_lib import *

# vordefinierte Funktionen wie nord(), sued(), etc. ... zum Bewegen der Figur
from moves import *

# aus der Datei client_lib.py alle Funktionen importieren
sys.path.append('../')
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

        elif befehl == "a":
            spawnen(game_client)

        elif befehl == "b":
            spawnen_x_mal(game_client, 10) # 10 x nacheinander spawnen

        elif befehl == "c":
            einen_schritt_nach(game_client, "nord")

        elif befehl == "d":
            schritte = 3
            richtung = "nord"
            n_schritte_nach(game_client, schritte, richtung)

        elif befehl == "e":
            einen_schritt_nach(game_client, "nord")

        elif befehl == "f":
            einen_schritt_nach_norden_und_einen_nach_nordwesten(game_client)

        else:
            game_client.publish(befehl)

        game_client.print_attribute()

""" Als 10. Aufgabe: lagern Sie die Funktionen einen_schritt_nach() in die Datei client_lib.py aus und importieren Sie diese Funktionen dann mit einem import-Befehl am Anfang dieses Programms wieder.
"""

def n_schritte_nach(game_client, n, richtung):
    """
    Als Neunte Aufgabe implementieren Sie eine Funktion, die Ihre Figur n Schritte in eine Richtung bewegt und ersetzen die Funktion n_schritte_nach_norden() damit.
    """

    for _ in range(n):
        einen_schritt_nach(game_client, richtung)


# Aufgabe 8 - vereinfachen sie diese Datei, indem Sie die Funktion einen_schritt_nach(game_client, richtung) überall dort nutzen, wo angebracht. Löschen Sie die unsicheren bzw. unnötigen Funktionen.


def einen_schritt_nach_norden_und_einen_nach_nordwesten(game_client):
    """
    Als sechste Aufgabe bewegen Sie Ihre Figur einen Schritt nach Norden und anschliessend einen Schritt nach Nordenwesten, ohne von der Spielflaeche zu fallen.

    Nutzen Sie die Bibliotheksfunktionen

    nord(x, y)
    nord_west(x, y)

    """
    einen_schritt_nach(game_client, "nord")
    einen_schritt_nach(game_client, "nord_west")

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
