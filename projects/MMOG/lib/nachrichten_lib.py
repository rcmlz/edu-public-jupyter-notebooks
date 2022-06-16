#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from time import sleep
from threading import Thread

try: # Python 3.x
    from queue import Empty
except ImportError: # Python 2.7
    from Queue import Empty

def initialisiere_subscription(spiel):
    subscription = set()
    kanal = spiel["conf"]["subscribe_to"]
    for spieler in spiel["spieler"].keys():
        subscription.add((spieler + "/" + kanal, 0))
    return subscription

def sender(shutdown_flag, client, postausgang, kanal):
    """
    If there are messages in the postausgang queue - send them
    """
    while not shutdown_flag.isSet():
        try:
            message = postausgang.get(timeout=1)
            chan = message[0] + "/" + kanal
            msg = message[1]
            client.publish(chan, msg)
        except Empty as inst:
            pass
        else:
            postausgang.task_done()

# see https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
def nachrichten(shutdown_flag, config, spiel, posteingang, postausgang):
    """
    To Do
    """
    # erzeugt einen Thread, der on_message alles in den Posteingang schaufelt ...
    client = connect(config, posteingang, spiel)
    client.loop_start()
    
    send = Thread(name="sender", target=sender, args=(shutdown_flag, client, postausgang, spiel["conf"]["publish_to"]))
    send.daemon = True
    send.start()
    
    shutdown_flag.wait()
    
    send.join()

    client.loop_stop(force=True)
    client.disconnect()

def on_message(client, userdata, message):
    """
    We put the messages in a shared, thread save queue
    """
    kanal = userdata["spiel"]["conf"]["subscribe_to"]
    n = -1 * (len(kanal) + 1) # + 1 wegen /
    userdata["posteingang"].put((message.topic[0:n], message.payload))
    
def on_connect(client, userdata, flags, rc):
    print("Verbindung mit {} auf Port {}: {}".format(userdata["broker"],userdata["port"],mqtt.connack_string(rc)))
    kanale_qos = initialisiere_subscription(userdata["spiel"])
    client.subscribe(list(kanale_qos))

def on_subscribe(client, userdata, mid, granted_qos):
    kanale_qos = initialisiere_subscription(userdata["spiel"])
    l = [x[0] for x in list(kanale_qos)]
    print("Topics: {}".format(l))

def on_publish(client, userdata, mid):
    print("Published")
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
          
def connect(config, posteingang, spiel):
    """
    To Do
    """
    client = mqtt.Client(userdata={"spiel": spiel, "posteingang": posteingang, "broker": config["MQTT"]["broker"], "port" : config["MQTT"]["port"]})
    if "user" in config["MQTT"].keys() and "password" in config["MQTT"].keys():
        client.username_pw_set(config["MQTT"]["user"], password=config["MQTT"]["password"])
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    #client.on_publish = on_publish
    client.on_message = on_message
    client.connect(config["MQTT"]["broker"], port = int(config["MQTT"]["port"]))
    return client