#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import shuffle
from Queue import Empty
from time import sleep
from threading import Thread

from common_lib import *

import sys
sys.path.append('../')
from server_gehirn import gehirn

sys.path.append('../../lib/')
from moves import *
from befehle import *

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
    global befehle
    
    re_spawner = Thread(name="respawn", target=re_spawn, args=(shutdown_flag, re_spawn_flag, spiel, posteingang))
    re_spawner.daemon = True
    re_spawner.start()

    while not shutdown_flag.isSet():
        try:
            spieler, befehl = posteingang.get(timeout=1)
            
            befehl_stripped, parameter = zerteile(befehl, spiel)
            
            if befehl_stripped in befehle.keys():
                
                spiel["spieler"][spieler]["max_x"] = spiel["conf"]["max_x"]
                spiel["spieler"][spieler]["max_y"] = spiel["conf"]["max_y"]

                ergebnis = {}
                ergebnis['befehl'] = befehl
                ergebnis['new_pos'] = None
                ergebnis['new_life'] = None
                ergebnis['antwort'] = None

                parameter_check_ok, err_msg = parameter_is_valid(parameter, befehle, befehl_stripped)
                if parameter_check_ok:
                    gehirn(spiel, spieler, ergebnis, befehl_stripped, parameter)
                else:
                    ergebnis['antwort'] = err_msg
                    
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
#        finally:

    re_spawner.join()

def update_spiel(spiel, spieler, result):
    spiel["spieler"][spieler]["befehl"] = result['befehl']
    spiel["spieler"][spieler]["antwort"] = result['antwort']

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
        
        if spiel["conf"]["trennzeichen"] in befehl and len(befehl) > 2:
            splitted = (befehl.split(spiel["conf"]["trennzeichen"]))
            if isinstance(splitted, list) and len(splitted) > 1: # wir haben Parameter
                if len(splitted[1]) > 2 and trennzeichen_parameter in splitted[1] and spiel["conf"]["trennzeichen"] not in [splitted[1][0], splitted[1][-1]]: #es gibt mind. 2 Parameter
                    par = splitted[1].split(trennzeichen_parameter)
                    b = splitted[0]
                    p = par
                else:
                    b = splitted[0]
                    p = splitted[1][0] #nur der erste buchstabe
        return (b, (p))
    
    except Exception as inst:
        print("Fehler zerteile(): {}".format(inst))
