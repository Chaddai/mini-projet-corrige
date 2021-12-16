# -*- coding: utf-8 -*-
from constantes import *


def init_ecran():
    """Initialise l'affichage Pygame en plein écran et renvoie la résolution et la surface d'affichage"""
    pygame.init()
    # On récupère les informations d'affichage actuelle
    infoEcran = pygame.display.Info()
    (LARGEUR, HAUTEUR) = (infoEcran.current_w, infoEcran.current_h)

    # on se met en mode plein écran avec la résolution actuelle
    return LARGEUR, HAUTEUR, pygame.display.set_mode((LARGEUR, HAUTEUR), FULLSCREEN)


def gestion_evenements(monde):
    """Gère les événements et modifie le monde ou affecte l'interface"""
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            monde.running = False
        elif event.type == KEYDOWN and event.key in DIRECTIONS:
            monde.move_perso(DIRECTIONS[event.key])


horloge = pygame.time.Clock()


def limite_fps(frames_par_seconde):
    """
    Bloque pendant le temps nécessaire pour que 1/frames_par_seconde s se
    soit écoulé depuis le dernier appel.
    """
    horloge.tick(frames_par_seconde)
