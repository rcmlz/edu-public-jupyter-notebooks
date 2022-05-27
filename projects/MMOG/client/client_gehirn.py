from time import sleep
from random import randint
import sys
sys.path.append('../lib/')
from moves import *

def random_walk(game_client, schritte):
    game_client.refresh_attribute()# durch absetzen des move Befehls weden die Attribute in der Schleife automatisch aktualisiert
    
    for i in range(schritte):
        attribute = game_client.attribute()
        
        neues_x = attribute["position"][0] + randint(-1, 1)
        neues_y = attribute["position"][1] + randint(-1, 1)

        if 0 <= neues_x < attribute["max_x"] and 0 <= neues_y < attribute["max_y"]:
            befehl = "move{}{},{}".format(game_client.trennzeichen, neues_x, neues_y)
            print("######\nVersuche Bewegung {} -> {}\n######".format(attribute["position"], (neues_x, neues_y)))
            game_client.publish(befehl)

        sleep(1)
