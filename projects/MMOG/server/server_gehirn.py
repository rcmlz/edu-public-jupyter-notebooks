#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint

import sys
sys.path.append('lib')
from common_lib import *
sys.path.append('../lib/')
sys.path.append('../../lib/')
from moves import *
from befehle import *

def gehirn(spiel, spieler, ergebnis, befehl, parameter=None):

    new_msg = "OK"
    new_life = None
    new_pos = None

    max_x = spiel["spieler"][spieler]["max_x"]
    max_y = spiel["spieler"][spieler]["max_y"]

    if befehl == "help":
        return help(ergebnis)

    elif befehl == "status": # status wird immer mit zurückgegeben - ausser bei help
        pass

    elif befehl == "spawn":
        new_pos=initialisiere_position(spiel)
        new_life=100

    elif befehl == "harakiri":
        new_pos=(None, None)
        new_life=0

    elif befehl == "move":
        x_new, y_new = parameter
        x_old, y_old = spiel["spieler"][spieler]["position"]

        x_old, y_old = int(x_old), int(y_old)
        x_new, y_new = int(x_new), int(y_new)
        max_x, max_y = int(max_x), int(max_y)

        if not 0 <= x_new < max_x or not 0 <= y_new < max_y:
            new_pos=(None, None)
            new_life=0
            new_msg = "{} ist ausserhalb des Spielfeldes {} - du bist tot!".format((x_new, y_new), (max_x, max_y))

        elif x_old == None and y_old == None:
            new_msg = "Du lebst ja nicht - please spawn"

        elif x_new == x_old and y_new == y_old:
            new_msg = "Du stehst schon auf Position {}".format((x_new, y_new))

        elif (x_new, y_new) not in positionen(spiel):

            if not ist_nah_genug(x_old, y_old, x_new, y_new):
                new_msg = "Position {} ist zu weit entfernt vom Standort {}".format((x_new, y_new), (x_old, y_old))
            else:
                new_pos=(x_new, y_new)
                new_life= spiel["spieler"][spieler]["leben"] - 1

        elif (x_new, y_new) in positionen(spiel):
            new_msg = "Position {} ist besetzt".format((x_new, y_new))

        else:
            print("Nanu ... wie kommen wir den hier hin? server_gehirn()")

    ergebnis['new_pos'] = new_pos
    ergebnis['new_life'] = new_life
    ergebnis['antwort'] = new_msg

    return ergebnis

def ist_nah_genug(x_old, y_old, x_new, y_new):
    """
    Berechnet, ob eine Bewegung auf die neuen Koordinaten erlaubt ist

    >>> ist_nah_genug(2, 7, 2, 5)
    True
    >>> ist_nah_genug(2, 7, 3, 6)
    True
    >>> ist_nah_genug(2, 7, 3, 8)
    True
    >>> ist_nah_genug(2, 7, 2, 9)
    True
    >>> ist_nah_genug(2, 7, 2, 8)
    True
    >>> ist_nah_genug(2, 7, 2, 6)
    True
    >>> ist_nah_genug(2, 7, 1, 5)
    False
    >>> ist_nah_genug(2, 7, 2, 4)
    False
    >>> ist_nah_genug(2, 7, 2, 3)
    False
    >>> ist_nah_genug(2, 7, 3, 4)
    False
    >>> ist_nah_genug(2, 7, 3, 5)
    False
    >>> ist_nah_genug(2, 7, 3, 7)
    False
    >>> ist_nah_genug(2, 7, 3, 9)
    False
    >>> ist_nah_genug(2, 7, 3, 10)
    False
    >>> ist_nah_genug(2, 7, 2, 11)
    False
    >>> ist_nah_genug(2, 7, 2, 10)
    False
    >>> ist_nah_genug(2, 7, 1, 9)
    False
    >>> ist_nah_genug(2, 7, 1, 4)
    False
    >>> ist_nah_genug(2, 7, 1, 3)
    False
    >>> ist_nah_genug(2, 7, 2, 2)
    False
    >>> ist_nah_genug(1, 12, 2, 13)
    False
    >>> ist_nah_genug(1, 10, 2, 11)
    False
    >>> ist_nah_genug(2, 10, 3, 11)
    False
    """
    moegliche_felder = (nord(x_old, y_old), sued(x_old, y_old), nord_west(x_old, y_old), sued_west(x_old, y_old), nord_ost(x_old, y_old), sued_ost(x_old, y_old))
    return (x_new, y_new) in moegliche_felder

def initialisiere_position(spiel):
    """
    To Do
    """
    taken = positionen(spiel)
    forbidden = forbidden_positions(3, spiel["conf"]["max_y"])
    pos = (None, None)
    while pos in forbidden or pos in taken:
        pos = (randint(0, spiel["conf"]["max_x"] - 1), randint(0, spiel["conf"]["max_y"] - 1))
    return pos


def help(ergebnis):
    global befehle
    new_msg = ""
    for befehl, attribute in befehle.items():
        new_msg = new_msg + "\n\t" + befehl + " - " + attribute["doc"]
    ergebnis['antwort'] = new_msg + "\n"
    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
