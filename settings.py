# -*- coding: utf-8 -*-

# GAME SETTINGS
MAX_LEVEL = 20   # > 1
GAME_NORMAL_SPEED = 40
GAME_SPEED_BOOST = 5
GOLD = 100
HP = 7200

# CREEPS SETTINGS
INIT_CREEPS = {
    "mob1": [5, 100, 1],
    "mob2": [2, 500, 1],
    "mob3": [7, 350, 1],
    "boss1": [0.7, 1000, 1],
    "boss2": [0.75, 1250, 1.05],
    "boss3": [0.8, 1550, 1.1],
    "andra": [0.85, 2000, 1.2]
}

# TURRETS SETTINGS
BASE_TURRET_COST = 40
INIT_TURRETS = {
    # range, upgrade cost, damage, slow duration, speed modifier, skin, number type
    "Base": [100, 40, 10, 0, 1, 0, 0, 0],
    "Gaz Lacrymogènes": [100, 123, 10, 50, 0.5, 1, 1, 1],
    "Portée": [150, 123, 40, 0, 1, 3, 4, 4],
    "Dommages": [100, 123, 30, 0, 1, 2, 3, 3],
    "Seb": [200, 123, 100, 50, 0.5, 4, 4, 4]
}

# UI SETTINGS
IMG_ROOT = "./images"
FRAME_HEIGHT = 600
FRAME_WIDTH = 800
UI_HEIGHT = 150
PADDING = 1
NB_CRENEAUX = 5
PATH_WIDTH = 40
TREE_COUNT = 4
TURRET_WIDTH = 50

INIT_UI = {
    "start":    {"text": "Start/Pause", "coords": (186, 49), "font": "Purisa"},
    "speedup":  {"text": "Vitesse++/Normal", "coords": (616, 49), "font": "Purisa"},
    "message":  {"var": "messageVar", "coords": (401, 88), "font": "Purisa"},
    "vague":    {"var": "vagueVar", "coords": (160, 121), "font": "Purisa"},
    "hp":       {"var": "hpVar", "coords": (320, 121), "font": "Purisa"},
    "gold":     {"var": "goldVar", "coords": (500, 121), "font": "Purisa"},
    "score":    {"var": "scoreVar", "coords": (640, 121), "font": "Purisa"}
}
