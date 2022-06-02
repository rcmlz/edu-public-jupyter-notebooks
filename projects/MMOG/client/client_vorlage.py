# Imports
import sys
# im lib-Ordner finden sie ggf. interessante Funktionen, die sie benutzen können (und die auch der Server nutzt)
sys.path.append('../lib/')
from game_client_lib import *
from moves import *

# falls wir Funktionen auslagern wollen (und damit leichter testbar machen), könnten wir diese  z.B. 
# in der Datei client_gehirn.py speichern, hier im Beispiel random_walk()
from client_gehirn import *

# Settings
spieler = "some_player_name@somewhere.org"

# Programm
game_client = Game_Client(spieler, "../config/config.json")

while True:
    nachricht = input("Befehl? (z.B.: help)", False)  # False: wenn "Abbrechen" geklickt wird, wird None zurückgegeben

    if nachricht in [None,":bye"]:
        break  # while Schleife verlassen

    elif nachricht == "a":
        attribute = game_client.attribute()
        print("Aktuelle Attribute: {}".format(attribute))

    elif nachricht == "r":
        random_walk(game_client, 10)

    else:
        game_client.publish(nachricht)

game_client.disconnect()
