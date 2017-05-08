# -*- coding: utf-8 -*-

import collections
import random
from math import sqrt

from models.model_airejeu import AireJeu
from models.model_tour import Tour
from models.model_vague import Vague
from settings import *


class Partie:
    def __init__(self, controller):
        self.parent = controller

        # --- init params
        self.niveauMax = MAX_LEVEL
        self.hauteur_aire = FRAME_HEIGHT
        self.largeur_aire = FRAME_WIDTH
        self.hauteur_ui = UI_HEIGHT
        self.nb_creneaux = NB_CRENEAUX
        self.largeur_sentier = PATH_WIDTH
        self.tree_count = TREE_COUNT
        self.taille_tour = TURRET_WIDTH
        self.padding = PADDING
        self.creep_database = INIT_CREEPS
        self.tour_database = INIT_TURRETS
        self.uidb = INIT_UI

        self.intro_closed = False
        self.boite_clic_intro = [265, 504, 536, 545]
        self.liste_tour = []
        self.trees = []
        self.reset_vars()

        self.aireJeu = AireJeu(self, self.largeur_aire, self.hauteur_aire, self.nb_creneaux, self.largeur_sentier,
                               self.taille_tour, self.padding)
        self.place_trees(self.tree_count, self.aireJeu.tailleMini)

    def reset_vars(self):
        self.niveau = 1
        self.layout_vague = collections.OrderedDict()
        self.vague_en_attente = None
        self.vague_en_marche = []
        self.mort = []
        self.paused = False
        self.score = 0
        self.gold = GOLD
        self.hp = HP
        self.prixTour = BASE_TURRET_COST
        self.win_or_lose_showed = False
        self.tour_selected = None
        self.double_speed = False

    def start(self):
        self.reset_vars()
        self.pop_niveau_courant()
        self.parent.vue.show_message("Des grévistes se dirigent vers le Cégep !")
        self.parent.vue.canevas.delete("layer 61")

    def update_game(self):
        if self.intro_closed:
            if not self.paused:
                if self.double_speed:
                    self.parent.frequence_cycles = GAME_SPEED_BOOST
                else:
                    self.parent.frequence_cycles = GAME_NORMAL_SPEED
                self.check_next_pop()
                self.check_vitesse_creeps()
                self.deplace_creeps()
                self.tours_check_cibles()
                self.check_creeps_swiped()
            if self.hp <= 0 and not self.win_or_lose_showed:
                self.win_or_lose_showed = True
                self.paused = True
                self.parent.vue.show_looser_screen()

    def pop_niveau_courant(self):
        if self.niveau >= self.niveauMax:
            self.win_or_lose_showed = True
            self.paused = True
            self.parent.vue.show_winning_screen()
        else:
            # premiere vague
            if len(self.layout_vague) == 0:
                self.layout_vague["mob1"] = 10
                self.layout_vague["mob2"] = 1

            if self.niveau in range(2, 5):
                self.layout_vague["mob1"] += 3

            if self.niveau == 5:  # 19 mobs1 et 1 mob2
                del self.layout_vague["mob2"]
                self.layout_vague["boss1"] = 1

            if self.niveau == 6:
                del self.layout_vague["boss1"]
                self.layout_vague["mob1"] = 10
                self.layout_vague["mob2"] = 5

            if self.niveau in range(7, 10):
                self.layout_vague["mob1"] += 3
                self.layout_vague["mob2"] += 1

            if self.niveau == 10:
                self.layout_vague["boss2"] = 1

            if self.niveau in range(11, 15):
                self.layout_vague["mob1"] += 2
                self.layout_vague["mob2"] += 1
                self.layout_vague["boss2"] = 0

            if self.niveau == 15:
                self.layout_vague["boss1"] = 3
                self.layout_vague["boss2"] = 1
            if self.niveau == 15:
                self.layout_vague["boss1"] = 0
                self.layout_vague["boss2"] = 0
                self.layout_vague["mob3"] = 1

            if self.niveau in range(17, 25):
                self.layout_vague["mob1"] += 5

                self.layout_vague["mob2"] += 3
                self.layout_vague["mob3"] += 1

            if self.niveau == 25:
                self.layout_vague["mob1"] = 0
                self.layout_vague["mob2"] = 0
                self.layout_vague["mob3"] = 0
                self.layout_vague["boss3"] = 1

            if self.niveau == 26:
                self.layout_vague["boss3"] = 0
                self.layout_vague["mob1"] = 15
                self.layout_vague["mob2"] = 15
                self.layout_vague["mob3"] = 10
                self.layout_vague["boss1"] = 2

            if self.niveau in range(27, 35):
                self.layout_vague["mob1"] += 7
                self.layout_vague["mob2"] += 5
                self.layout_vague["mob3"] += 2
                self.layout_vague["boss1"] += 1

            if self.niveau == 35:
                self.layout_vague["mob1"] = 0
                self.layout_vague["mob2"] = 0
                self.layout_vague["mob3"] = 0
                self.layout_vague["boss1"] = 10
                self.layout_vague["boss2"] = 8
                self.layout_vague["boss3"] = 5

            if self.niveau == 36:
                self.layout_vague["boss2"] = 0
                self.layout_vague["boss3"] = 0
                self.layout_vague["mob1"] = 25
                self.layout_vague["mob2"] = 20
                self.layout_vague["mob3"] = 15

            if self.niveau in range(37, 40):
                self.layout_vague["mob1"] += 7
                self.layout_vague["mob2"] += 5
                self.layout_vague["mob3"] += 3
                self.layout_vague["boss1"] += 2
                self.layout_vague["boss2"] += 1

            if self.niveau == 40:
                self.layout_vague["mob1"] = 0
                self.layout_vague["mob2"] = 0
                self.layout_vague["mob3"] = 0
                self.layout_vague["boss1"] = 0
                self.layout_vague["boss2"] = 0
                self.layout_vague["andra"] = 1

            if self.niveau == 41:
                self.layout_vague["andra"] = 0
                self.layout_vague["mob1"] = 35
                self.layout_vague["mob2"] = 25
                self.layout_vague["mob3"] = 20
                self.layout_vague["boss1"] = 7
                self.layout_vague["boss2"] = 5
                self.layout_vague["boss3"] = 2

            if self.niveau in range(42, 50):
                self.layout_vague["mob1"] += 7
                self.layout_vague["mob2"] += 5
                self.layout_vague["mob3"] += 3
                self.layout_vague["boss1"] += 3
                self.layout_vague["boss2"] += 2
                self.layout_vague["boss3"] += 1

            if self.niveau == 50:
                self.layout_vague["mob1"] = 75
                self.layout_vague["mob2"] = 55
                self.layout_vague["mob3"] = 35
                self.layout_vague["boss1"] = 15
                self.layout_vague["boss2"] = 10
                self.layout_vague["boss3"] = 5
                self.layout_vague["andra"] = 2

            self.layout_vague["pop_frequency"] = 100 - (self.niveau * 2)
            self.vague_en_attente = Vague(self, self.layout_vague)
            self.mort = []

    # ------ GESTION DES CREEPS
    def pop_un_creep(self):
        if self.vague_en_attente.is_not_empty():
            self.vague_en_marche.append(self.vague_en_attente.get_next_creep())

    def deplace_creeps(self):
        for i in self.vague_en_marche:
            i.deplace()

    @staticmethod
    def creep_takes_damage(creep, degats, speed_mod, slow_duration):
        creep.prendre_projectile(degats, speed_mod, slow_duration)

    def creep_dies(self, c):
        if c in self.vague_en_marche:
            self.mort.append(c)
            self.vague_en_marche.remove(c)
            self.score += 1
            self.gold += 2

    def check_vitesse_creeps(self):
        for i in self.vague_en_marche:
            if i.slow_duration > 0:
                i.change_speed()

    def cegep_perd_un_point(self):
        if self.hp > 0:
            self.hp -= 72

    # décompte avant pop du prochain creep
    def check_next_pop(self):
        if self.vague_en_attente is not None:
            if self.vague_en_attente.pop_frequency > 0:
                self.vague_en_attente.pop_frequency -= 1
            elif self.vague_en_attente.pop_frequency == 0:
                self.pop_un_creep()
                self.vague_en_attente.pop_frequency = self.frequence_de_pop_courante

    def check_creeps_swiped(self):
        if self.vague_en_attente is not None:
            if len(self.vague_en_attente.creep_list) == 0 and len(self.vague_en_marche) == 0:
                # niveau suivant
                self.niveau += 1
                self.pop_niveau_courant()

    # ------ GESTION DES TOURS
    def placer_tour(self, x, y):
        if self.position_tour_valide(x, y) and self.gold >= self.prixTour:
            self.liste_tour.append(Tour(self, x, y))
            self.gold -= self.prixTour
        else:
            self.parent.vue.show_message("Vous n'avez pas assez d'argent pour acheter un gardien(40CR)")
        self.parent.vue.close_turret_popup()

    def get_tour_database(self):
        return self.tour_database

    def supprimer_tour(self, une_tour):
        pass

    # fonction qui va déterminer si l'argent est suffisant pour upgrader
    # va pointer sur la bonne tour correspondante dans la liste
    def upgrade_tour(self, type_upgrade, turret):
        if self.gold >= turret.prix_upgrade:
            turret.upgrade(type_upgrade)
        else:
            self.parent.vue.show_message(
                "Vous n'avez pas assez d'argent pour l'upgrade(" + str(turret.prix_upgrade) + "CR)")

    def tours_check_cibles(self):
        for t in self.liste_tour:
            t.find_target()

    def position_tour_valide(self, x, y):
        return self.dans_zone_jeu_moins_marge_tours(x, y)\
                and not self.sur_le_sentier_plus_marge_tour(x, y) \
                and not self.overlap_tour(x, y)

    def dans_zone_jeu_moins_marge_tours(self, x, y):
        m = self.taille_tour / 2 + self.padding + 20  # 20 : largeur de la bordure, si on la garde....
        x_min = m
        y_min = m
        x_max = self.largeur_aire - m
        y_max = self.hauteur_aire - m
        return self.point_dans_boite(x, y, [x_min, y_min, x_max, y_max])

    def sur_le_sentier_plus_marge_tour(self, x, y):
        for z in self.aireJeu.zonesExclusionSentier:
            if self.point_dans_boite(x, y, [z[0], z[1], z[2], z[3]]):
                return True
        return False

    def point_dans_boite(self, x, y, boite):
        # boite de type [x_min,y_min,x_max,y_max]
        x_min = boite[0]
        y_min = boite[1]
        x_max = boite[2]
        y_max = boite[3]
        return x_min <= x <= x_max and y_min <= y <= y_max

    def overlap_tour(self, x, y):
        for t in self.liste_tour:
            boite = self.carre_autour_dun_point(t.x, t.y, self.taille_tour + self.padding)  # 2 demi tours + 1 marge
            if self.point_dans_boite(x, y, boite):
                return True
        for coords in self.trees:
            boite = self.carre_autour_dun_point(coords[0], coords[1],
                                                self.taille_tour + self.padding)  # 2 demi tours + 1 marge
            if self.point_dans_boite(x, y, boite):
                return True
        return False

    def sur_une_tour(self, x, y):
        for t in self.liste_tour:
            boite = self.carre_autour_dun_point(t.x, t.y, self.taille_tour / 2)
            if self.point_dans_boite(x, y, boite):
                return t
        return None

    # ------ ARBRES

    def place_trees(self, nb_trees, taille_mini):
        min_x = self.largeur_aire / self.nb_creneaux
        max_x = self.largeur_aire - self.largeur_aire / self.nb_creneaux
        min_y = taille_mini
        max_y = self.hauteur_aire - taille_mini

        for i in range(nb_trees):
            valide = False
            while not valide:
                x = random.randint(min_x, max_x)
                y = random.randint(min_y, max_y)
                valide = self.position_tour_valide(x, y)
            self.trees.append([x, y])

        return self.trees

    # --- Gestion des events
    # fonction qui gère les clicks gauche sur le canevas

    def check_event_left_click(self, event_x, event_y):
        if not self.intro_closed:
            if self.point_dans_boite(event_x, event_y, self.boite_clic_intro):
                self.close_intro()
        else:
            if self.niveau < self.niveauMax and self.hp > 0:  # si on a pas encore gagné ou perdu
                if self.clic_sur_aire(event_x, event_y):
                    # on commence en détruisant tout pop up indésirable 
                    if self.parent.vue.menu_confirm_popup:
                        self.parent.vue.close_turret_popup()
                    if self.parent.vue.upgrade_popup:
                        self.parent.vue.close_turret_upgrade_popup()

                    if self.sur_une_tour(event_x, event_y) is None:
                        if self.position_tour_valide(event_x, event_y):
                            self.parent.vue.open_turret_popup(event_x, event_y)
                        else:
                            self.parent.vue.show_message("Vous ne pouvez pas placer de gardien ici")
                    else:
                        self.parent.vue.show_message(
                            "Cette position n'est pas valide, vous êtes déjà sur un gardien !")
                elif self.clic_sur_u_i(event_x, event_y):
                    if self.point_dans_boite(event_x, event_y, [90, self.hauteur_aire + 32, 283, self.hauteur_aire + 65]):
                        if self.vague_en_attente is None:  # on a pas commencé la partie
                            self.start()
                        else:
                            self.toggle_pause()

                    elif self.point_dans_boite(event_x, event_y,
                                               [304, self.hauteur_aire + 32, 498, self.hauteur_aire + 65]):
                        pass
                    elif self.point_dans_boite(event_x, event_y,
                                               [519, self.hauteur_aire + 32, 713, self.hauteur_aire + 65]):
                        self.speed_up()
            else:  # si on a gagné ou perdu
                if self.point_dans_boite(event_x, event_y, [90, self.hauteur_aire + 32, 283, self.hauteur_aire + 65]):
                    self.liste_tour = []
                    self.start()

    def speed_up(self):
        print("speed me up")
        self.double_speed = not self.double_speed

    # fonction qui gère les clicks droits sur le canevas visant à upgrader une tour
    def check_event_right_click(self, event_x, event_y):
        if self.intro_closed:
            if self.clic_sur_aire(event_x,
                                  event_y) and self.niveau < self.niveauMax and self.hp > 0:  # si on a pas encore gagné:
                # on commence en détruisant tout pop up indésirable 
                if self.parent.vue.menu_confirm_popup is not None:
                    self.parent.vue.close_turret_popup()
                if self.parent.vue.upgrade_popup is not None:
                    self.parent.vue.close_turret_upgrade_popup()

                # maintenant on vérifie si on est bel et bien sur une tour
                if self.sur_une_tour(event_x, event_y) is not None:
                    self.tour_selected = self.sur_une_tour(event_x, event_y)
                    self.parent.vue.open_turret_upgrade_popup(event_x, event_y, self.tour_selected)
                else:
                    self.parent.vue.show_message("Clic droit - Vous devez cliquer sur un gardien pour l'améliorer.")

    def clic_sur_aire(self, x, y):
        return self.point_dans_boite(x, y, [2, 2, 2 + self.largeur_aire, 2 + self.hauteur_aire])

    def clic_sur_u_i(self, x, y):
        return self.point_dans_boite(x, y, [2, 2 + self.hauteur_aire, 2 + self.largeur_aire,
                                            2 + self.hauteur_aire + self.hauteur_ui])

    # appel à la vue pour fermer le menu       
    def upgrade_fini(self):
        self.parent.vue.close_turret_upgrade_popup()

    # ------ METHODES UTILITAIRES
    def close_intro(self):
        self.intro_closed = True

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.parent.vue.show_message("Prenez le temps de respirer un coup, la menace de la grève plane toujours")
        else:
            self.parent.vue.show_message("Des grévistes se dirigent vers le Cégep !")

            # passe le sentier a ton voisin!
            # transmet le sentier hors du modèle où qu'il soit dans celui-ci

    def get_sentier(self):
        return self.aireJeu.sentier

    def get_vue(self):
        return self.parent.vue

    # distance entre 2 points
    @staticmethod
    def get_dist(ptA, ptB):
        # ptA et ptB de type [x,y]
        return sqrt((ptA[0] - ptB[0]) ** 2 + (ptA[1] - ptB[1]) ** 2)

    # renvoie les limites d'un carré de côté size*2 et de centre (x,y)
    @staticmethod
    def carre_autour_dun_point(x, y, size):
        x_min = x - size
        y_min = y - size
        x_max = x + size
        y_max = y + size
        return [x_min, y_min, x_max, y_max]
