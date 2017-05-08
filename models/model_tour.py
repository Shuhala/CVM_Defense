# -*- coding: utf-8 -*-

import random

from helpers.helper import Helper as H


class Tour:
    def __init__(self, partie, x, y):
        self.parent = partie
        self.taille = self.parent.taille_tour
        self.x = x
        self.y = y
        self.projectiles = []
        self.niveau_tour = 1

        # va chercher les paramètres de la tour dans le dictionnaire situé dans partie
        # portée,prix, degat,slowduration, speedmod,tour skin et projectileskin correspondant
        data_tour = self.parent.get_tour_database()
        self.type_tour = data_tour["Base"]
        self.portee = self.type_tour[0]
        self.prix_upgrade = self.type_tour[1]
        self.degats = self.type_tour[2]
        self.slow_duration = self.type_tour[3]
        self.speed_mod = self.type_tour[4]
        self.skin_tour = self.type_tour[5]
        self.numero_type = self.type_tour[7]

        self.frequence_tir = 10  # cycles MAX entre 2 tirs = vitesse lente
        # self.vitesseDeTir le modifie!
        self.delai_avant_tir_suivant = 0

    def find_target(self):
        targets = []
        for i in self.parent.vague_en_marche:  # Pour chaque creep dans la vague
            d = H.calc_distance(self.x, self.y, i.x, i.y)  # Prendre sa distance
            if d <= self.portee:
                targets.append(i)
        if targets:
            choix = random.choice(targets)  # On choisi une cible al�atoire � tirer
            if self.delai_avant_tir_suivant == 0:
                self.attack(choix)
                self.delai_avant_tir_suivant = self.frequence_tir

        if self.delai_avant_tir_suivant > 0:
            self.delai_avant_tir_suivant -= 1

        hit = []
        for i in self.projectiles:  # Pour chaque projectile on le deplace
            i.deplace()
            if i.x == i.ciblex:  # Si la cible est � port�e, on le tire
                hit.append(i)
        for i in hit:
            self.projectiles.remove(i)  # Lorsque le projectile a touch� sa cible, on l'enl�ve de la liste

    def attack(self, creep):
        self.projectiles.append(Projectile(self, self.parent, creep))

    # On upgrade la tour en fonction de l'upgrade choisi
    def upgrade(self, upgrade_type):
        if upgrade_type == "Dommages":
            self.degats += 50
            self.type_tour = self.parent.tour_database[upgrade_type]

        elif upgrade_type == "Portée":
            self.portee += 100
            self.type_tour = self.parent.tour_database[upgrade_type]

        elif upgrade_type == "rof":
            pass

        elif upgrade_type == "Gaz Lacrymogènes":
            self.slow_duration = 50
            self.speed_mod -= 0.2
            self.type_tour = self.parent.tour_database[upgrade_type]

        self.niveau_tour += 1
        self.parent.gold -= self.prix_upgrade
        self.prix_upgrade *= 2
        self.parent.upgrade_fini()


class Projectile:
    def __init__(self, parent, partie, c):
        self.parent = parent
        self.vitesse = 10
        self.partie = partie
        self.x = parent.x
        self.y = parent.y
        self.c = c  # on conserve la trace du creep cible de l'obus
        self.ciblex = c.x
        self.cibley = c.y
        self.angle = H.calc_angle(self.x, self.y, c.x, c.y)
        self.degats = self.parent.degats
        self.slow_duration = self.parent.slow_duration
        self.speed_mod = self.parent.speed_mod
        self.skin_projectile = self.parent.type_tour[6]

    def deplace(self):
        d = H.calc_distance(self.x, self.y, self.ciblex, self.cibley)
        if d > self.vitesse:
            self.x, self.y = H.get_angled_point(self.angle, self.vitesse, self.x, self.y)
        else:
            self.x = self.ciblex
            self.y = self.cibley
            self.explose()

    def explose(self):
        self.partie.creep_takes_damage(self.c, self.degats, self.speed_mod, self.slow_duration)
