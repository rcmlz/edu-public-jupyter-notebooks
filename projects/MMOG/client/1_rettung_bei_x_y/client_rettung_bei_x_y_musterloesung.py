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
        befehl = input("Befehl? (z.B.: help|status|spawn|harakiri|move#x,y)", False)  # TigerJython: False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben
        #befehl = input("Befehl? (z.B.: help|status|spawn|harakiri|move#x,y)\n")  # Thonny Editor

        if befehl in (None,":bye"):
            break  # while Schleife verlassen

        elif befehl == "r":
            rettung_bei_x_y(game_client, 0, 0)

        else:
            game_client.publish(befehl)

        game_client.print_attribute()


def rettung_bei_x_y(game_client, x_ziel = 0, y_ziel = 0):
    """
    Die Figur beweg sich so schnell wie moeglich zu den Zielkoordinaten (default 0,0).

    """
    # zunächst einmal die Attribute aktualisieren, damit wir wissen, wo wir stehen.
    game_client.publish("status")

    # geplaner Algorithmus:
    # solange, bis man im Ziel 0,0 ist: (ausser wenn wir hoffnungslos feststecken, dann neu spawnen und neu versuchen)
    # - erst so weit wie moeglich nach nord_west,
    # - dann so weit wie moeglich nach nord,
    # - dann sued_west,
    # - dann wieder so weit wie moeglich nach nord_west usw.

    # damit wir wissen, wann wir neu spawnen muessen
    hoffnung = 3

    # die Reihenfolge der Richtungen, die wir laufen, bis wir feststecken

    # ToDo: dieser Algorithmus klappt nicht immer, da die Funktion
    # einen_schritt_nach() ist nicht perfekt ist, da man immer noch im
    # Osten und Sueden von der Spielfläche fallen kann.
    richtungen = ("nord_west", "nord", "sued_west")

    # aktueller Standort
    attribute = game_client.attribute()
    x_aktuell, y_aktuell = attribute["position"]

    ziel_erreicht = x_aktuell == x_ziel and y_aktuell == y_ziel

    while not ziel_erreicht:
        for richtung in richtungen: # so lange in eine Richtung laufen, bis wir feststecken

            # aktueller Standort
            attribute = game_client.attribute()
            x_aktuell, y_aktuell = attribute["position"]

            stecke_fest = False
            while not stecke_fest:
                # x_alt, y_alt werden nach dem move verwendet, um festzustellen, ob wir feststecken.
                x_alt, y_alt = x_aktuell, y_aktuell

                # jetzt in die aktuelle Richtung laufen
                einen_schritt_nach(game_client, richtung)

                # wo stehen wir nach dem Move?
                attribute = game_client.attribute()
                x_aktuell, y_aktuell = attribute["position"]

                # Abbruchbedingung der while-schleife aktualisieren
                stecke_fest = x_alt == x_aktuell and y_alt == y_aktuell

                # damit wir auf der Konsole sehen, was los ist ...
                game_client.print_attribute()

            # bevor wir in eine neue Richtung laufen, erstmal schauen, ob wir nicht doch schon am Ziel sind und den for-loop verlassen koennen.
            ziel_erreicht = x_aktuell == x_ziel and y_aktuell == y_ziel
            if ziel_erreicht:
                break

        # Falls wir hoffnungslos feststecken, brechen wir ab, re-spawnen und probieren es nochmal von der neuen Position aus.
        hoffnung -= 1
        if hoffnung < 1 and not ziel_erreicht:
            game_client.publish("spawn")
            hoffnung = 3


##############################################################
# Programm
##############################################################
manuelle_steuerung(game_client)

##############################################################
# aufräumen - game_client abmelden bevor das Programm endet
game_client.disconnect()
