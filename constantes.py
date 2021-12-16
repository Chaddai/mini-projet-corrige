# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from pathlib import Path

MUR = 1
VIDE = 0
OBSTACLE = 2

TUILES_DIM = ((0, 50), (101, 131))

# dictionnaire des sprites à charger avec les coordonnées de leur "centre" à faire
# correspondre aux coordonnées du "centre de la tuile" (50, 90)
SPRITES = {
    "Star": (48, 100),
    "Tree Short": (48, 130),
    "Tree Tall": (48, 130),
    "Character Boy": (50, 134),
}

PERSO = "Character Boy"

DIRECTIONS = {
    K_RIGHT: (1, 0),
    K_LEFT: (-1, 0),
    K_UP: (0, -1),
    K_DOWN: (0, 1),
}
