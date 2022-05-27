from random import shuffle, randint

def positionen(spiel):
    """
    To Do
    """
    pos = set()
    for daten in spiel["spieler"].values():
        pos.add(daten["position"])
    return pos

def forbidden_positions():
    forbidden = set()
    forbidden.add((0,0))
    forbidden.add((None, None))
#    forbidden.add((0,2))
#    forbidden.add((0,1))
#    forbidden.add((0,4))
#    forbidden.add((0,3))
#    forbidden.add((1,0))
#    forbidden.add((1,2))
#    forbidden.add((0,6))
#    forbidden.add((0,5))
#    forbidden.add((1,4))
#    forbidden.add((1,3))
#    forbidden.add((1,1))
#    forbidden.add((0,8))
#    forbidden.add((0,7))
#    forbidden.add((1,6))
#    forbidden.add((1,5))
#    forbidden.add((2,4))
#    forbidden.add((2,2))
#    forbidden.add((2,0))
    return forbidden

def initialisiere_spieler(config):
    """
    To Do
    """
    spieler_datei = config["spieler_datei"]
    symbole_datei = config["symbole_datei"]

    symbole = []
    with open(symbole_datei) as text_datei:
        for zeile in text_datei:
            symbole.append(zeile.rstrip())

    shuffle(symbole)
    count_icons = len(symbole)
    id_icon = 0

    emails = set()
    with open(spieler_datei) as text_datei:
        for zeile in text_datei:
            emails.add(zeile.rstrip())

    gamers = {}
    available_felder = config["SPIELFELDER_VERTIKAL"] * config["SPIELFELDER_HORIZONTAL"]
    if len(emails) <= available_felder - len(forbidden_positions()):
        for email in emails:
            gamers["{}/{}".format(config["game_name"],email)] = {
                    "bild": symbole[id_icon % count_icons],
                    "position": (None, None),
                    "leben": 0,
                }
            id_icon += 1
    else:
        print("To many players")

    return gamers
