# -*- coding: utf-8 -*-
from pygame import color
from constantes import *
from gestion_pygame import init_ecran
from labyrinthes import fabrique_labyrinthe
import random


class Monde:
    def __init__(self, TL, TH):
        self.running = True
        self.LARGEUR, self.HAUTEUR, self.ECRAN = init_ecran()
        self.font = pygame.font.SysFont(
            ["comicsansms", "timesnewroman", "sourcesans", None], size=32, bold=True
        )

        # constantes relatives aux tuiles et à leurs dimensions sur l'écran
        self.TL, self.TH = TL, TH
        self.GTL, self.GTH = self.LARGEUR // TL, self.HAUTEUR // TH
        self.laby = fabrique_labyrinthe(TL, TH)

        ((_x_hd, y_hd), (_x_bg, y_bg)) = TUILES_DIM
        self.yfacteur = self.GTH / (y_bg - y_hd)
        self.charge_tuiles("images")
        self.ydecalage = TUILES_DIM[0][1] * self.yfacteur

        # Initialise le tableau des décorations et charge les images des sprites
        self.decorations = [[[] for _ix in range(TL)] for _iy in range(TH)]
        self.charge_sprites("images")

        # Place les objets dans le labyrinthe
        self.place_perso()
        self.decore()

    ## Affichage
    def affiche(self):
        self.affiche_labyrinthe()
        self.affiche_compteurs()
        self.affiche_decorations()

    def affiche_labyrinthe(self):
        for iy in range(self.TH):
            for ix in range(self.TL):
                img = self.tuiles["Grass"]
                if self.laby[iy][ix] == MUR:
                    img = self.tuiles["Water"]
                elif self.laby[iy][ix] == OBSTACLE:
                    img = self.tuiles["Dirt"]
                self.ECRAN.blit(img, self.ix2coords(ix, iy))

    def affiche_decorations(self):
        for iy in range(self.TH):
            for ix in range(self.TL):
                for deco in self.decorations[iy][ix]:
                    img = self.sprites[deco]
                    pos = self.ix2coords(ix, iy, delta=self.sprites_delta[deco])
                    self.ECRAN.blit(img, pos)

    def affiche_compteurs(self):
        """Affiche les compteurs de trésors/étoiles/... capturés"""
        star = self.sprites["Star"]
        star = pygame.transform.smoothscale(
            star, (star.get_width() // 2, star.get_height() // 2)
        )
        (xc, yc) = SPRITES["Star"]
        self.ECRAN.blit(star, (self.GTL // 4 - xc // 2, self.GTH // 4 - yc // 2))

        texte = self.font.render("x " + str(self.capture), True, "black")
        self.ECRAN.blit(texte, (self.GTL // 2, 0))

    ## Gestion des personnages/monstres
    def move_perso(self, direction):
        """Déplace le personnage dans la direction donnée, si c'est possible.
        Gère la capture des trésors/étoiles/..."""
        pos_depuis = self.perso_pos
        (ixd, iyd) = pos_depuis
        depuis = self.decorations[iyd][ixd]

        pos_vers = (ixd + direction[0], iyd + direction[1])
        (ixv, iyv) = pos_vers
        vers = self.decorations[iyv][ixv]

        if self.accessible(pos_vers):
            self.perso_pos = pos_vers
            depuis.remove(PERSO)
            vers.append(PERSO)

            if "Star" in vers:
                vers.remove("Star")
                self.capture += 1
                self.stars -= 1

            return True

        return False

    ## Utilitaires
    def ix2coords(self, ix, iy, delta=(0, 0)):
        return (ix * self.GTL + delta[0], iy * self.GTH - self.ydecalage + delta[1])

    def accessible(self, pos):
        ix, iy = pos
        return 0 <= ix < self.TL and 0 <= iy < self.TH and self.laby[iy][ix] == VIDE

    def isolee(self, pos):
        ix, iy = pos
        return self.laby[iy][ix] == MUR and all(
            self.accessible((ix + dx, iy + dy)) for (dx, dy) in DIRECTIONS.values()
        )

    ## Placements des objets sur le labyrinthe
    def decore(self):
        self.stars = 0
        self.capture = 0
        for iy in range(self.TH):
            for ix in range(self.TL):
                pos = (ix, iy)
                if self.isolee(pos):
                    arbre = random.choice(["Tree Short", "Tree Tall"])
                    self.laby[iy][ix] = OBSTACLE
                    self.decorations[iy][ix].append(arbre)
                if self.accessible(pos) and pos != self.perso_pos:
                    if random.random() < 0.1:
                        self.stars += 1
                        self.decorations[iy][ix].append("Star")

    def place_perso(self):
        self.perso_pos = (0, 0)
        while not self.accessible(self.perso_pos):
            self.perso_pos = (
                random.randrange(0, self.TL),
                random.randrange(0, self.TH),
            )
        (ixv, iyv) = self.perso_pos
        self.decorations[iyv][ixv].append(PERSO)

    ## Chargement des ressources
    def charge_tuiles(self, dir):
        p = Path(dir)
        self.tuiles = dict()
        for fichier in p.glob("* Block.png"):
            img = pygame.image.load(fichier)
            (L, H) = img.get_size()
            # ajuste les dimensions pour que l'écran soit à peu près rempli de tuiles
            # attention, selon les TL et TH choisis, ceci peut déformer les tuiles
            (NL, NH) = self.GTL, int(H * self.yfacteur)
            # retire " Block" à la fin du nom de fichier
            self.tuiles[fichier.stem[:-6]] = pygame.transform.smoothscale(img, (NL, NH))

    def charge_sprites(self, dir):
        p = Path(dir)
        self.sprites = dict()
        self.sprites_delta = dict()
        for nom in SPRITES:
            img = pygame.image.load(p / (nom + ".png"))
            xcenter, ycenter = SPRITES[nom]
            delta = (50 - xcenter, 90 - ycenter)
            (L, H) = img.get_size()
            (NL, NH) = self.GTL, int(H * self.yfacteur)
            self.sprites[nom] = pygame.transform.smoothscale(img, (NL, NH))
            self.sprites_delta[nom] = delta
