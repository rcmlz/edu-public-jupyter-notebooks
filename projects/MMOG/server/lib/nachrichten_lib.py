#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from time import sleep
from threading import Thread
from Queue import Empty

def initialisiere_subscription(spiel):
    subscription = set()
    for spieler in spiel["spieler"].keys():
        subscription.add((spieler, 0))
    return subscription

def sender(shutdown_flag, client, postausgang):
    """
    If there are messages in the postausgang queue - send them
    """
    while not shutdown_flag.isSet():
        try:
            message = postausgang.get(timeout=1)
            client.publish(message[0], message[1])
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
    client = connect(config, spiel, posteingang)
    client.loop_start()
    
    send = Thread(name="sender", target=sender, args=(shutdown_flag, client, postausgang))
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
    if "{'msg': 're:" not in message.payload and "HELP" not in message.payload:
        userdata["posteingang"].put((message.topic, message.payload))

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+ mqtt.connack_string(rc))
    kanale_qos = initialisiere_subscription(userdata["spiel"])
    client.subscribe(list(kanale_qos))

def on_subscribe(client, userdata, mid, granted_qos):
    kanale_qos = initialisiere_subscription(userdata["spiel"])
    print("Subscribed {}".format(list(kanale_qos)))

def on_publish(client, userdata, mid):
    print("Published")
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
          
def connect(config, spiel, posteingang):
    """
    To Do
    """
    client = mqtt.Client(userdata={"spiel": spiel, "posteingang": posteingang})
    client.username_pw_set(config["MQTT"]["user"], password=config["MQTT"]["password"])
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    #client.on_publish = on_publish
    client.on_message = on_message
    client.connect(config["MQTT"]["broker"], port = config["MQTT"]["port"])
    return client