# -*- coding: utf-8 -*-
import random
from constantes import MUR, VIDE


def fabrique_labyrinthe(largeur, hauteur):
    """
    Cette fonction retourne un labyrinthe dont les dimensions sont
    largeur x hauteur.

    ATTENTION: ces nombres doivent être IMPAIRS (de la forme 2n+1)
    et au moins égaux à trois.

    Le labyrinthe est une matrice (un tableau de tableau), contenant
    des entiers, suivant la convention suivante:

    - 0: case vide (le sol sur lequel on peut marcher)
    - 1: un mur (ou de l'eau, selon l'interprétation que l'on en
      fait). Bref: une case inaccessible.


    Utilise l'algorithme décrit sur la page wikipedia:
    http://fr.wikipedia.org/wiki/Modélisation_mathématique_d'un_labyrinthe#Exploration_exhaustive
    """

    # On s'assure que les largeurs et hauteurs spécifiées répondent au
    # cahier des charges:
    # Imparité:
    assert largeur % 2 == 1
    assert hauteur % 2 == 1
    # Valeur minimale:
    assert largeur >= 3
    assert hauteur >= 3

    largeur_reelle = (largeur - 1) / 2
    hauteur_reelle = (hauteur - 1) / 2

    # On commence par créer un labyrinthe aux bonnes dimensions,
    # toutes les cases sont initialement à 1 (mur). Notre algorithme
    # va litéralement "creuser" des couloirs dans ces murs.
    laby = [[MUR] * largeur for n in range(hauteur)]

    # La première case à creuser
    debut = (1, 1)
    # Le nombre de cases à creuser en tout.
    compteur = hauteur_reelle * largeur_reelle

    # on utilisera une Liste python pour notre pile, où
    # append() et pop() ajoute ou retire un élément au sommet
    # on lit le sommet sans le retirer (peek) à l'indice -1 : pile[-1]
    pile = [debut]
    while compteur > 0:
        # On récupère le dernier élément de la pile. Il est toujours
        # sous la forme (ligne, colonne), ou encore (y, x) avec des
        # notations mathématiques standard.
        y, x = pile[-1]

        # Si la position courante n'est pas encore creusée, on le
        # fait.
        if laby[y][x] == MUR:
            laby[y][x] = VIDE
            compteur = compteur - 1

        # À partir de la position courante, on examine les 4
        # directions cardinales et on regarde s'il est possible de
        # creuser par là (la case d'arrivée, 2 positions plus loin, ne
        # doit pas déjà être creusée). Il faut aussi éviter de sortir
        # des limites du tableau, d'où les nombreux tests.
        directions_possibles = []
        for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (
                (dy == -1 and y > 1)
                or (dy == 1 and y < hauteur - 2)
                or (dx == -1 and x > 1)
                or (dx == 1 and x < largeur - 2)
            ):
                if laby[y + 2 * dy][x + 2 * dx] == MUR:
                    # La case de destination est pleine: on peut y
                    # aller.
                    directions_possibles.append((dy, dx))
                else:
                    # La case de destination est déjà utilisée, on ne
                    # peut à priori pas y aller. On s'autorise tout de
                    # même le passage dans 20% des cas, afin de créer
                    # des boucles dans le labyrinthe.
                    if random.random() >= 0.8:
                        directions_possibles.append((dy, dx))

        if len(directions_possibles) == 0:
            # Aucune direction n'est possible à partir du point
            # courant (c'est un cul-de-sac). On "dépile" le dernier
            # élément de notre pile pour revenir un cran en arrière (=
            # on rebrousse chemin).
            pile.pop()
        else:
            # Il existe des directions vers lesquelles on peut
            # creuser. On en choisit donc une au hasard en utilisant
            # la fonction standard random.choice que l'on a importée
            # en début de programme.
            (dy, dx) = random.choice(directions_possibles)
            # On creuse le mur choisi
            laby[y + dy][x + dx] = VIDE
            # Et on empile la nouvelle position que l'on vient
            # d'atteindre.
            pile.append((y + 2 * dy, x + 2 * dx))

    return laby


def print_labyrinthe(laby):
    # Cette fonction attend en entrée un labyrinthe généré par la
    # fonction make_laby, et l'imprime de manière relativement
    # esthétique. On utilise des dièses # pour les murs et des espaces
    # pour le sol.
    for ligne in laby:
        for n in ligne:
            if n == 0:
                print(" ", end="")
            elif n == 1:
                print("#", end="")
        print()
    print()


# On n'exécute la ligne suivante que si le fichier est directement
# lancé par l'utilisateur, pas lorsqu'il est importé en tant que
# librairie.
if __name__ == "__main__":
    print_labyrinthe(fabrique_labyrinthe(15, 9))
