#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys # damit "lib/moves.py" importiert werden kann
sys.path.append('../lib/')
from moves import * # vordefinierte Funktionen zum Bewegen der Figur

from time import sleep # mit sleep() könnte man nach jedem Zug oder Fehlversuch eine bestimmte Zeit warten
from random import randint # randint() könnte man ggf. für drunken_sailor nutzen

##############################################################
# HIER IHRE EIGENEN ALGORITHMEN IMPLEMENTIEREN
#
# als Vorlage ein paar nützliche Befehle und Beispielcode ...
##############################################################

def rettung_bei_x_y(game_client, x_ziel = 0, y_ziel = 0):
    """ 
    Bewegt die eigene Figur zu den Ziel-Koordinaten x,y = (0,0)
    
    """
    
    # Figur-Attribute aktualisieren und in lokaler Variablen speichern.
    # In der Variablen attribute steht nun, auf welchen Koordinaten wir derzeit stehen, 
    # wieviele Lebenspunkte wir noch haben, etc.
    attribute = game_client.attribute()
    
    # auslesen aus dem Dictionary "attribute", wo wir selbst gerade stehen
    x = attribute["position"][0]
    y = attribute["position"][1]
    
    # neue Position berechnen
    neues_x = x
    neues_y = y
    
    # "move#x,y"-Befehl an Server senden, damit unsere Figur sich auf die berechnete, neue Position bewegt
    befehl = "move{}{},{}".format(game_client.trennzeichen, neues_x, neues_y)
    game_client.publish(befehl)
    
    # warten ... vielleicht wollen Sie den anderen ja eine Chance geben ... ;-)
    sleep(1)


def drunken_sailor(game_client, schritte = 100):
    """ 
    Bewegt die eigene Figur zufällig übers Spielfeld, ohne über den Rand bei max_x und max_y zu fallen.
    
    """
    pass