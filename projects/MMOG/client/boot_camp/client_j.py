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

def n_schritte_nach(game_client, n, richtung):
    """
    Als Neunte Aufgabe implementieren Sie eine Funktion, die Ihre Figur n Schritte in eine Richtung bewegt und ersetzen die Funktion n_schritte_nach_norden() damit.
    """

    for _ in range(n):
        einen_schritt_nach(game_client, richtung)


# Aufgabe 8 - vereinfachen sie diese Datei, indem Sie die Funktion einen_schritt_nach(game_client, richtung) überall dort nutzen, wo angebracht. Löschen Sie die unsicheren bzw. unnötigen Funktionen.

def einen_schritt_nach(game_client, richtung):
    """
    Als siebente Aufgabe sollen Sie die Funktionen einen_sicheren_schritt_nach_nord_westen() und einen_sicheren_schritt_nach_norden() wegen Code Duplication
    durch eine Funktion ersetzen, welche die Richtung als Parameter entgegennimmt.

    Nutzen Sie die Bibliotheksfunktionen

    nord(x, y)
    sued(x, y)
    nord_west(x, y)
    sued_west(x, y)
    nord_ost(x, y)
    sued_ost(x, y)
    """

    # Auslesen der aktuellen Position aus den Attributen
    attribute = game_client.attribute()
    x_aktuell = attribute["position"][0]
    y_aktuell = attribute["position"][1]

    # Berechnung der Zielkoordinaten
    x_neu, y_neu = None, None

    if richtung == "nord":
        x_neu, y_neu = nord(x_aktuell, y_aktuell)
    elif richtung == "sued":
        x_neu, y_neu = sued(x_aktuell, y_aktuell)
    elif richtung == "nord_west":
        x_neu, y_neu = nord_west(x_aktuell, y_aktuell)
    elif richtung == "sued_west":
        x_neu, y_neu = sued_west(x_aktuell, y_aktuell)
    elif richtung == "nord_ost":
        x_neu, y_neu = nord_ost(x_aktuell, y_aktuell)
    elif richtung == "sued_ost":
        x_neu, y_neu = sued_ost(x_aktuell, y_aktuell)

    # und absetzen des entsprechenden move#x,y Befehls
    # aber nur, wenn x_neu und y_neu nicht None
    if x_neu != None and y_neu != None:
        # oder negativ sind
        if x_neu >= 0 and y_neu >= 0:
            befehl = "move#{},{}".format(x_neu, y_neu)
            game_client.publish(befehl)


def einen_schritt_nach_norden_und_einen_nach_nordwesten(game_client):
    """
    Als sechste Aufgabe bewegen Sie Ihre Figur einen Schritt nach Norden und anschliessend einen Schritt nach Nordenwesten, ohne von der Spielfläche zu fallen.

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
