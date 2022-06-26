#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import shuffle, randint

def positionen(spiel):
    """
    To Do
    """
    pos = set()
    for daten in spiel["spieler"].values():
        pos.add(daten["position"])
    return pos

def forbidden_positions(x_max, y_max):
    forbidden = set()
    forbidden.add((None, None))
    for x in range(x_max):
        for y in range(y_max):
            forbidden.add((x,y))
    return forbidden


def parameter_is_valid(parameter, befehle, befehl):
    erwartet = None

    if "anzahl_parameter" in befehle[befehl].keys():
        erwartet = befehle[befehl]["anzahl_parameter"]
    
    if parameter is None and erwartet is None:
        return (True, "OK")
    elif parameter is None:
        err_msg = "Fehler in Befehl: '{}'. Parameter fehlt! Doc: {})".format(befehl, befehle[befehl]["doc"])
        return (False, err_msg)
    
    gegeben = len(parameter)
    if gegeben != erwartet:
        err_msg = "Fehler in Befehl: '{}'. Gegeben: {} Erwartet: {} Doc: {})".format(befehl, gegeben, erwartet, befehle[befehl]["doc"])
        return (False, err_msg)
        
    return (True, "OK")


def initialisiere_spieler(config):
    """
    To Do
    """
    spieler_datei = config["spieler_datei"]
    symbole_datei = config["symbole_datei"]

    symbole = []
    with open(symbole_datei) as text_datei:
        for zeile in text_datei:
            symbole.append(zeile.rstrip())

    shuffle(symbole)
    count_icons = len(symbole)
    id_icon = 0

    emails = set()
    with open(spieler_datei) as text_datei:
        for zeile in text_datei:
            emails.add(zeile.rstrip())

    gamers = {}
    available_felder = config["SPIELFELDER_VERTIKAL"] * config["SPIELFELDER_HORIZONTAL"]
    if len(emails) <= available_felder - len(forbidden_positions(3, config["SPIELFELDER_VERTIKAL"])):
        for email in emails:
            gamers["{}/{}".format(config["game_name"],email)] = {
                    "bild": symbole[id_icon % count_icons],
                    "position": (None, None),
                    "leben": 0,
                }
            id_icon += 1
    else:
        print("To many players")

    return gamers
