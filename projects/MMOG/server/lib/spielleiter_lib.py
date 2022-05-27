#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import shuffle
from Queue import Empty
from time import sleep
from threading import Thread

from common_lib import *

import sys
sys.path.append('../')
from server_gehirn import gehirn, befehle

sys.path.append('../../lib/')
from moves import *

def re_spawn(shutdown_flag, re_spawn_flag, spiel, posteingang):
    while not shutdown_flag.isSet():
        re_spawn_flag.wait(timeout=1)
        if re_spawn_flag.isSet():
            re_spawn_flag.clear()
            for spieler in spiel["spieler"].keys():
                posteingang.put((spieler, "spawn"))

def spielleiter(shutdown_flag, anzeige_aktualisieren_flag, re_spawn_flag, spiel, posteingang, postausgang):
    """
    To Do
    """
    re_spawner = Thread(name="respawn", target=re_spawn, args=(shutdown_flag, re_spawn_flag, spiel, posteingang))
    re_spawner.daemon = True
    re_spawner.start()

    while not shutdown_flag.isSet():
        try:
            spieler, befehl = posteingang.get(timeout=1)
            
            befehl, parameter = zerteile(befehl, spiel)
            if befehl in befehle.keys():
                spiel["spieler"][spieler]["max_x"] = spiel["conf"]["max_x"]
                spiel["spieler"][spieler]["max_y"] = spiel["conf"]["max_y"]

                ergebnis = {}
                ergebnis['source'] = 'SERVER'
                ergebnis['new_pos'] = None
                ergebnis['new_life'] = None
                ergebnis['new_msg'] = None

                gehirn(spiel, spieler, ergebnis, befehl, parameter)

                if befehl == "help":
                   reply = "\nHELP\n" + ergebnis['new_msg']
                else:
                    ergebnis['new_msg'] = "re: " + ergebnis['new_msg']
                
                    # update_spiel() gibt True zurück, falls Positionen oder Leben aktualisiert wurde
                    if update_spiel(spiel, spieler, ergebnis):
                        anzeige_aktualisieren_flag.set()
 
                    reply = str(spiel["spieler"][spieler])

                postausgang.put((spieler, reply))
                        
        except Empty as inst:
            pass
        except Exception as inst:
            print("Fehler: spielleiter() {} : {} : {}".format(spieler, befehl, inst))
        else: # nothing went wrong
            posteingang.task_done()

    re_spawner.join()

def update_spiel(spiel, spieler, result):
    spiel["spieler"][spieler]["msg"] = result['new_msg']

    updated = False
    if result['new_pos'] is not None:
        spiel["spieler"][spieler]["position"] = result['new_pos']
        updated = True

    if result['new_life'] is not None:
        spiel["spieler"][spieler]["leben"] = result['new_life']
        updated = True

    return updated

def zerteile(befehl, spiel):
    trennzeichen_parameter = ","
    try:
        b = befehl
        p = None
        
        if spiel["conf"]["trennzeichen"] in befehl and len(befehl) > 2 and spiel["conf"]["trennzeichen"] not in [befehl[0], befehl[-1]]: # nicht nur befehl + trennzeichen
            splitted = befehl.split(spiel["conf"]["trennzeichen"])
            if trennzeichen_parameter in splitted[1] and len(splitted[1]) > 2 and spiel["conf"]["trennzeichen"] not in [splitted[1][0], splitted[1][-1]]: #es gibt mind. 2 Parameter
                par = splitted[1].split(trennzeichen_parameter)
                if len(par) == befehle[splitted[0]]["anzahl_parameter"]:
                    b = splitted[0]
                    p = par
            else:
                b = splitted[0]
                p = splitted[1]

        return (b, p)
    except Exception as inst:
        print("Fehler zerteile(): {}".format(inst))
