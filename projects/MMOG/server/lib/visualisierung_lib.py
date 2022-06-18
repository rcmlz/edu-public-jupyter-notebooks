#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ein wildes gehacke, das man unbdingt aufraeumen muss
"""
from time import sleep
from math import sin, radians, ceil
from gturtle import *
from common_lib import *

SPIELFELDER_VERTIKAL = 16
SPIELFELDER_HORIZONTAL = int(ceil(SPIELFELDER_VERTIKAL / 3))

PADDING = 10
SEITENLAENGE = 50
ECKEN = 6

DREHWINKEL = 360 / ECKEN

GAMMA = 90
ALPHA = DREHWINKEL / 2
SIN_ALPHA = sin(radians(ALPHA))
BETA = GAMMA - ALPHA
SIN_BETA = sin(radians(BETA))
C = SEITENLAENGE
A = SEITENLAENGE * SIN_ALPHA
B = SEITENLAENGE * SIN_BETA
D = 2**0.5 * C
E = (C**2 + D**2) ** 0.5

SEITENLEISTE = 400

PANEL_BREITE = SPIELFELDER_VERTIKAL * SEITENLAENGE + SEITENLEISTE + PADDING
PANEL_HOEHE = SPIELFELDER_VERTIKAL * SEITENLAENGE + PADDING

LINKS_OBEN_X = -1 * PANEL_BREITE / 2 + PADDING + A
LINKS_OBEN_Y = PANEL_HOEHE / 2 - PADDING

RECHTS_OBEN_X = PANEL_BREITE / 2 - PADDING
RECHTS_OBEN_Y = PANEL_HOEHE / 2 - PADDING

X_SHIFT = 2 * (A + C)
Y_SHIFT = B

Options.setPlaygroundSize(PANEL_BREITE, PANEL_HOEHE)
# TF = TurtleFrame()
# STIFT = Turtle(TF)
STIFT = None
STIFT = makeTurtle()
STIFT.ht()
STIFT.enableRepaint(False)
STIFT.setFontSize(10)

def visualisierung(shutdown_flag, anzeige_aktualisieren_flag, config, spiel):
    """
    To Do
    """
    STIFT.setTitle("MMOG - Massive Multiuser Online Game - {} x {}".format(SPIELFELDER_VERTIKAL, SPIELFELDER_HORIZONTAL))
    STIFT.addStatusBar(30)
    STIFT.drawImage("resources/tribute.jpg")
    if config["MQTT"].has_key("user") and config["MQTT"].has_key("password"):
        STIFT.setStatusText(
            "Connect via MQTT to {} port: {} user: {} password: {} on topic: {}/your.email@kantiolten.ch and execute 'help' and 'spawn' command!".format(
                config["MQTT"]["broker"], config["MQTT"]["port"], config["MQTT"]["user"], config["MQTT"]["password"], config["game_name"]
            )
        )
    else:
        STIFT.setStatusText(
            "Connect via MQTT to {} port: {} on topic: {}/your.email@kantiolten.ch and execute 'help' and 'spawn' command!".format(
                config["MQTT"]["broker"], config["MQTT"]["port"], config["game_name"]
            )
        )

    STIFT.repaint()

    while not shutdown_flag.isSet():
        try:
            anzeige_aktualisieren_flag.wait(timeout=1) # falls das auf True gesetzt ist, geht es ohne 1 Sek Pause weiter
            if anzeige_aktualisieren_flag.is_set():
                anzeige_aktualisieren_flag.clear()
                try:
                    STIFT.clear()
                    zeichne(spiel["spieler"])
                    STIFT.repaint()
                except Exception as inst:
                    print("Fehler: {}".format(inst))
        except:
            pass

def zeichne(spiel):
        zeichne_hintergrund()
        zeichne_seitenleiste(spiel)
        zeichne_spieler(spiel)

        #playTone([("c", 700),("e", 1500)], instrument="trumpet")
        #playTone([("c", 700),("e", 1500)], instrument="organ")
        #playTone([("c", 700),("e", 1500)], instrument="piano")
        #playTone([("c", 700),("e", 1500)], instrument="violin")
        #playTone([("d", 300),("e", 200),("d", 300),("c#", 400)], instrument="xylophone")

def zeichne_hintergrund():
    for y in range(SPIELFELDER_VERTIKAL):
        OFFSET = y % 2 * (C + A)
        for x in range(SPIELFELDER_HORIZONTAL):
            STIFT.setHeading(90)
            new_x = LINKS_OBEN_X + x * X_SHIFT + OFFSET
            new_y = LINKS_OBEN_Y - y * Y_SHIFT
            STIFT.setPos(new_x, new_y - 10)
            STIFT.label("({},{})".format(x, y))
            STIFT.setPos(new_x, new_y)
            for i in range(ECKEN):
                STIFT.fd(SEITENLAENGE)
                STIFT.rt(DREHWINKEL)

def zeichne_spieler(gamers, show_dead_gamers=False):
    for y in range(SPIELFELDER_VERTIKAL):
        OFFSET = y % 2 * (C + A)
        for x in range(SPIELFELDER_HORIZONTAL):
            STIFT.setHeading(90)
            new_x = LINKS_OBEN_X + x * X_SHIFT + OFFSET
            new_y = LINKS_OBEN_Y - y * Y_SHIFT
            STIFT.setPos(new_x, new_y)
            for email, werte in gamers.items():
                if werte["position"] is not (None, None) or show_dead_gamers:
                    if (x, y) == werte["position"]:
                        new_x_img = new_x + C / 2
                        new_y_img = new_y - D / 2
                        STIFT.setPos(new_x_img, new_y_img)
                        STIFT.setHeading(0)
                        STIFT.drawImage("sprites/" + werte["bild"])


def zeichne_seitenleiste(gamers, show_dead_gamers=False):
    STIFT.setHeading(0)
    zeile = 0
    offset_y = 50
    for email, werte in gamers.items():
        if show_dead_gamers or werte["leben"] > 0:
            STIFT.setPos(RECHTS_OBEN_X - 160, RECHTS_OBEN_Y - 20 - zeile * offset_y)
            STIFT.label(email)
            STIFT.setPos(RECHTS_OBEN_X - 200, RECHTS_OBEN_Y - 20 - zeile * offset_y)
            STIFT.drawImage("sprites/" + werte["bild"])
            zeile += 1
