#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast #to do: replace by json for security

from time import strftime, sleep
from json import load
from threading import Thread, Event

try: # Python 3.x
    from queue import Empty
    from queue import Queue as queue
except ImportError: # Python 2.7
    from Queue import Empty
    from Queue import Queue as queue

from nachrichten_lib import nachrichten
from befehle import *

attribute = {}
attribute_aktuell = Event()
attribute_aktuell.set()

class Game_Client:

    def __init__(self, spieler, config_file):
        global attribute, attribute_aktuell
        with open(config_file, 'r') as f:
            config = load(f)

        self.spiel = {
             "spieler" : {"{}/{}".format(config["game_name"],spieler): attribute}
            ,"conf" : {
                "game_name" : config["game_name"]
                ,"gamer_id" : spieler
                ,"subscribe_to" : "ohr"
                ,"publish_to" : "mund"
            }
        }

        # mit shutdown signalisieren wir allen Threads von diesem Main-Thread aus, dass sie terminieren sollen
        self.shutdown_flag = Event()

        # Thread-sicheres weiterleiten der eingehenden und ausgehenden Nachrichten
        self.posteingang = queue()
        self.postausgang = queue()

        self.threads = [
                    Thread(name="nachrichten", target=nachrichten, args=(self.shutdown_flag, config, self.spiel, self.posteingang, self.postausgang))
                    ,Thread(name="attribute_aktualisieren", target=attribute_aktualisieren, args=(self.shutdown_flag, self.posteingang))
                  ]

        for t in self.threads:
            t.daemon = True
            t.start()

        self.trennzeichen = config["trennzeichen"]
        self.client_send_sleep = config["client_send_sleep"]


    def print_attribute(self):
        global attribute
        """
        Gibt alle Attribute sortiert auf der Konsole aus.
        """
        out = "Keine Attribute gefunden - richtige E-Mail und Game-Server gesetzt? Fuehre 'status' aus und aktualisiere so deine Attribute!"
        if len(attribute.keys()) > 0:
            out = "\n" + "#" * 50 + "\n"
            for key in sorted(attribute):
                out += "{}: {}\n".format(key, attribute[key])
            out += "#" * 50
        print(out)


    def attribute(self):
        global attribute, attribute_aktuell

        if not "updated" in attribute.keys():
            self.refresh_attribute()

        try:
            t = 5
            if not attribute_aktuell.isSet():
                attribute_aktuell.wait(timeout=t)
        except Exception as inst:
            print("Error! Keine Nachricht vom Game-Server in {} sec empfangen: Attribute nicht aktualisiert!".format(t))

        return attribute

    def refresh_attribute(self):
        global attribute_aktuell
        attribute_aktuell.clear()
        self.publish("status") # status erfragt eine Nachricht vom Server, mit der die Attribute aktualisiert werden können


    def publish(self, message):
        global attribute_aktuell
        kanal = list(self.spiel["spieler"].keys())[0] #es gibt ja nur einen Spieler

        # wir wollen sicherstellen, dass die in der Antwort enthaltenen Attribute aktualisiert wurden.
        m = "move"
        lm = len(m)
        if message != "help" and ( message in befehle.keys() or message[0:lm] == m ):
            attribute_aktuell.clear()

        self.postausgang.put((kanal, message))
        sleep(self.client_send_sleep)


    def disconnect(self):
        self.shutdown_flag.set()
        for t in self.threads:
            t.join()


# Diese Funktion läuft in einem eigenen Thread und aktualisiert die Attribute - ToDo: remove global variable
def attribute_aktualisieren(shutdown_flag, posteingang):
    global attribute, attribute_aktuell
    while not shutdown_flag.isSet():
        try:
            kanal, message = posteingang.get(timeout=2)
            try:
                if not isinstance(message, str):
                    message = message.decode('UTF-8')
                payload = ast.literal_eval(message) #ToDo: hier ist ein Sicherheitsproblem ... das müsste man durch json-parsing ersetzen
            except Exception as inst:
                print(inst)
                print(message)
            else: # nothing went wrong
                attribute = payload
                attribute["updated"] = strftime('%Y-%m-%d %H:%M:%S')
                posteingang.task_done()
            finally:
                attribute_aktuell.set()

        except Empty as inst:
            pass
