#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import load
from Queue import Queue as queue
from threading import Thread, Event

import sys
sys.path.append('lib')
from common_lib import *

# den globalen lib-Folder einbinden
sys.path.append('../lib/')

from spielleiter_lib import spielleiter
from nachrichten_lib import nachrichten
from visualisierung_lib import visualisierung, SPIELFELDER_VERTIKAL, SPIELFELDER_HORIZONTAL

def main(conf_file):
    with open(conf_file, 'r') as f:
        config = load(f)

    # mit shutdown signalisieren wir allen Threads von diesem Main-Thread aus, dass sie terminieren sollen
    shutdown_flag = Event()

    # mit grafik_aktualisieren signalisieren wir, dass die Grafik aufwachen soll und die Anzeige aktualisieren soll
    anzeige_aktualisieren_flag = Event()

    # mit respawn signalisieren wir, dass alle Spieler neu initialisiert werden sollen
    re_spawn_flag = Event()

    # im Dict spiel speichern wir den Zustad des Spiels
    config["SPIELFELDER_VERTIKAL"] = int(SPIELFELDER_VERTIKAL)
    config["SPIELFELDER_HORIZONTAL"] = int(SPIELFELDER_HORIZONTAL)

    spiel = {
         "spieler" : initialisiere_spieler(config)
        ,"conf" : {
             "max_y" : int(SPIELFELDER_VERTIKAL)
            ,"max_x" : int(SPIELFELDER_HORIZONTAL)
            ,"subscribe_to" : "mund"
            ,"publish_to" : "ohr"
            ,"trennzeichen" : config["trennzeichen"]
        }
    }

    # Thread-sicheres weiterleiten der eingehenden und ausgehenden Nachrichten
    posteingang = queue()
    postausgang = queue()

    threads = [
                  Thread(name="spielleiter", target=spielleiter, args=(shutdown_flag, anzeige_aktualisieren_flag, re_spawn_flag, spiel, posteingang, postausgang))
                 ,Thread(name="nachrichten", target=nachrichten, args=(shutdown_flag, config, spiel, posteingang, postausgang))
                 ,Thread(name="visualisierung", target=visualisierung, args=(shutdown_flag, anzeige_aktualisieren_flag, config, spiel))
               ]

    for t in threads:
        t.daemon = True
        t.start()

    re_spawn = True
    while re_spawn:
        re_spawn = askYesNo("Nein = Spiel abbrechen\nJa = Spawn All", False)
        if re_spawn:
            re_spawn_flag.set()

    shutdown_flag.set()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main('../config/config.json')
