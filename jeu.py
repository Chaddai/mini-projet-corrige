# -*- coding: utf-8 -*-
from constantes import *
from gestion_monde import Monde
from gestion_pygame import gestion_evenements, limite_fps

monde = Monde(15, 9)

while monde.running:
    limite_fps(60)
    monde.affiche()
    pygame.display.flip()
    gestion_evenements(monde)

pygame.quit()
