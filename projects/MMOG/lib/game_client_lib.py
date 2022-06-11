#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast #to do: replace by json for security
from mqttclient import *
from time import strftime, sleep
from json import load
from threading import Event

attribute = {}
attribute_aktuell = Event()
attribute_aktuell.set()

class Game_Client:

    def __init__(self, spieler, config_file):
        with open(config_file, 'r') as f:
            config = load(f)

        self.spieler = spieler

        self.spiel = config["game_name"]
        self.mund = "{}/{}/mund".format(self.spiel,self.spieler)
        self.ohr = "{}/{}/ohr".format(self.spiel,self.spieler)
        self.trennzeichen = config["trennzeichen"]
        self.client_send_sleep = config["client_send_sleep"]
        
        self.client = self.setup_mqtt(config)

    def attribute(self):
        global attribute, attribute_aktuell
        
        if not attribute_aktuell.isSet():
            attribute_aktuell.wait()
        
        if not attribute.has_key("updated"):
            return self.refresh_attribute()
        
        return attribute

    def refresh_attribute(self):
        global attribute_aktuell, attribute
        attribute_aktuell.clear()
        self.publish("status") # status erfragt eine Nachricht vom Spielleiter, mit der die Attribute aktualisiert werden können
        return self.attribute()

    def publish(self, message):
        self.client.publish(self.mund, message)
        sleep(self.client_send_sleep)

    def disconnect(self):
        self.client.disconnect()

    def setup_mqtt(self, config):

            if config["MQTT"].has_key("user") and config["MQTT"].has_key("password"):
                client = MQTTClient(messageReceived=react, username=config["MQTT"]["user"], password=config["MQTT"]["password"])
            else:
                client = MQTTClient(messageReceived=react)

            if config["verbose"]:
                client.setVerbose(True)

            if config["MQTT"].has_key("port"):
                client.connect(host=config["MQTT"]["broker"], port=config["MQTT"]["port"])
            else:
                client.connect(host=config["MQTT"]["broker"])

            client.subscribe(self.ohr)

            if config["verbose"]:
                client.setVerbose(False)

            return client

def print_status(game_client):
    """
    Gibt alle Attribute sortiert auf der Konsole aus.
    """
    attribute = game_client.attribute()
    print("#" * 50)
    for key in sorted(attribute):
        print("{}: {}".format(key, attribute[key]))
    print("#" * 50)


# das folgende läuft via react() in einem eigenen Thread, deshalb die Hantiererei mit global ... nicht schön, aber erstmal ok
def react(topic, message):
    m = "{} : {}"
    #Wenn wir eine {...} Nachricht empfangen, steht da u.A. position und staerke drin, dass merken wir uns gleich
    if message[0] == "{" and message[-1] == "}":
        aktualisieren(message)
    else:
        print(m.format(topic, message))

def aktualisieren(message):
    global attribute, attribute_aktuell
    try:
        payload = ast.literal_eval(message) #ToDo: hier ist ein Sicherheitsproblem ... das müsste man durch json-parsing ersetzen
    except Exception as inst:
        print(inst)
        print(message)
    else:
        attribute = payload
        attribute["updated"] = strftime('%Y-%m-%d %H:%M:%S')
    finally:
        attribute_aktuell.set()