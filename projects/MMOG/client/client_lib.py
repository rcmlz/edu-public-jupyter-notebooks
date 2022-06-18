#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../../lib/')

# vordefinierte Funktionen wie nord(), sued(), etc. ... zum Bewegen der Figur
from moves import *

def einen_schritt_nach(game_client, richtung):
    """
    richtung in ("nord", "sued", "nord_west", "sued_west", "nord_ost", "sued_ost")
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


def spawnen(game_client):
    """
    Spawnt 1x - Funktion nur zur ANSCHAUUNG, wie game_client.publish() funktioniert.
    """
    befehl = "spawn"
    game_client.publish(befehl)
