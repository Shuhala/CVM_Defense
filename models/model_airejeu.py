# -*- coding: utf-8 -*-

import math
import random


class AireJeu:
    def __init__(self, controler, width, height, nb_creneaux, largeur_sentier, taille_tour, padding):
        self.parent = controler
        self.height = height
        self.width = width
        self.creneaux = nb_creneaux
        self.largeurSentier = largeur_sentier
        self.tailleTour = taille_tour
        self.padding = padding
        self.tailleMini = self.tailleTour + 2 * self.padding
        self.sentier = self.generer_sentier()
        self.zonesExclusionSentier = self.calcul_zones_exclusion_sentier()

    def generer_sentier(self):
        # generate 5 widthParts
        xs = self.generate_xs()
        # generate 5 rand ys
        ys = self.generate_ys()

        path = [[0, ys[0]]]

        for i in range(self.creneaux):
            path.append([xs[i + 1], ys[i]])
            if i != self.creneaux - 1:
                path.append([xs[i + 1], ys[i + 1]])

        return path

    def generate_xs(self):
        moyenne = math.floor(self.width / self.creneaux)
        basse = math.floor(self.width / (self.creneaux + 1))
        haute = math.floor(self.width / (self.creneaux - 1))
        parts = []
        total = 0

        for i in range(self.creneaux):
            min = basse
            max = haute
            if i != 0:
                if parts[i - 1] <= moyenne:
                    min = moyenne
                else:
                    max = moyenne
            parts.append(random.randint(min, max))
            total += parts[i]

        diff_moyenne = math.ceil((self.width - total) / self.creneaux)
        total = 0

        for i in range(self.creneaux):
            parts[i] += diff_moyenne
            total += parts[i]

        if total != self.width:
            parts[random.randint(0, self.creneaux - 1)] -= (total - self.width)

        out = [0]
        for i in range(self.creneaux):
            out.append(out[i] + parts[i]);

        return out

    def generate_ys(self):
        mid_range_min = int((self.height / 2) - self.tailleMini)
        mid_range_max = int((self.height / 2) + self.tailleMini)
        upper_range_min = self.tailleMini
        upper_range_max = mid_range_min
        lower_range_min = mid_range_max
        lower_range_max = self.height - self.tailleMini
        ys = []

        for i in range(self.creneaux):
            if i == 0 or i == self.creneaux - 1:
                ys.append(random.randrange(mid_range_min, mid_range_max))
            else:
                if ys[i - 1] <= self.height / 2:
                    ys.append(random.randrange(lower_range_min, lower_range_max))
                else:
                    ys.append(random.randrange(upper_range_min, upper_range_max))
        return ys

    # cree la liste des zones d'exclusions du sentier
    def calcul_zones_exclusion_sentier(self):
        dist = (self.largeurSentier / 2) + (self.tailleTour / 2) + self.padding
        zones_exclusion_sentier = []
        for i in range(0, len(self.sentier) - 1):
            x_min = self.sentier[i][0] - dist
            y_min = self.sentier[i][1] - dist
            x_max = self.sentier[i + 1][0] + dist
            y_max = self.sentier[i + 1][1] + dist
            if self.sentier[i][1] > self.sentier[i + 1][1]:  # le chemin va vers le haut
                y_min = self.sentier[i + 1][1] - dist  # idem
                y_max = self.sentier[i][1] + dist  # idem
            zones_exclusion_sentier.append([x_min, y_min, x_max, y_max])
        return zones_exclusion_sentier
