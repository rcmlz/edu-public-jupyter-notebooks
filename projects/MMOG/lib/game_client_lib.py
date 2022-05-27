#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast #to do: replace by json for security
from mqttclient import *
from time import sleep
import random
from json import load

attribute = {}
attribute_werden_aktualisiert = False

class Game_Client:

    def __init__(self, spieler, config_file):
        with open(config_file, 'r') as f:
            config = load(f)

        self.spieler = spieler

        self.spiel = config["game_name"]
        self.kanal = "{}/{}".format(self.spiel,self.spieler)
        self.trennzeichen = config["trennzeichen"]

        self.client = self.setup_mqtt(config)

    def attribute(self):
        global attribute
        
        while attribute_werden_aktualisiert:
            sleep(0.1)

        return attribute

    def refresh_attribute(self):
        global attribute_werden_aktualisiert, attribute
        attribute_werden_aktualisiert = True
        self.publish("status")# status erzeugt eine Nachricht, so dass die Attribute automatisch aktualisiert werden
        return self.attribute()

    def publish(self, message):
        self.client.publish(self.kanal, message)

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

            client.subscribe(self.kanal)

            if config["verbose"]:
                client.setVerbose(False)

            return client

# das folgende läuft via react() in einem eigenen Thread, deshalb die Hantiererei mit global ... nicht schön, aber erstmal ok
def react(topic, message):
    m = "{} : {}"
    print(m.format(topic, message))
    #Wenn wir eine {...} Nachricht empfangen, steht da u.A. position und staerke drin, dass merken wir uns gleich
    if message[0] == "{" and message[-1] == "}":
        aktualisieren(message)

def aktualisieren(message):
    global attribute, attribute_werden_aktualisiert
    attribute_werden_aktualisiert = True
    try:
        payload = ast.literal_eval(message) #ToDo: hier ist ein Sicherheitsproblem ... das müsste man durch json-parsing ersetzen
    except Exception as inst:
        print(inst)
        print(message)
    else:
        attribute = payload
    finally:
        attribute_werden_aktualisiert = False
