# -*- coding: utf-8 -*-


class Creep:
    def __init__(self, vague, type):
        self.parent = vague
        self.itineraire = list(self.parent.get_sentier())
        self.x = self.itineraire[0][0]
        self.y = self.itineraire[0][1]
        self.index_cible_courante = 1
        self.get_properties(type)
        self.slow_duration = 0
        self.current_speed = self.max_speed
        self.speedMod = 1

    # On va chercher l'info dans le dictionnaire de creeps dans partie
    def get_properties(self, type):
        database = self.parent.get_creep_db()
        self.max_speed = database[type][0]
        self.points_vie = database[type][1]
        self.armure = database[type][2]
        self.skin = type

    # fonction qui vérifie si la vitesse doit être changée ou pas : Une creep ralentie ne peut être ralentie davantage
    def change_speed(self):
        if self.current_speed < self.max_speed:
            self.slow_duration -= 1
        else:
            self.current_speed *= self.speedMod
            self.slow_duration -= 1
        if self.slow_duration <= 0:
            self.current_speed = self.max_speed

    def is_dead(self):
        return self.points_vie <= 0

    # fonction où le creep reçoit le projectile ; ses points de vie et sa vitesse(s'il y a lieu) sont affectés modifiés
    def prendre_projectile(self, nb_degats, speed_mod, slow_duration):
        self.points_vie -= nb_degats / self.armure
        self.speedMod = speed_mod
        self.slow_duration = slow_duration
        if self.is_dead():
            self.parent.creep_dies(self)

    def deplace(self):
        # preparation des cibles courantes et suivantes en vue des verifications
        cible_courante = self.itineraire[self.index_cible_courante]
        if cible_courante != self.itineraire[-1]:
            cible_suivante = self.itineraire[self.index_cible_courante + 1]
        else:
            cible_suivante = None
        y_temp = self.y
        x_temp = self.x

        if self.x == cible_courante[0]:  # on move suivant axe y
            if cible_courante[1] < self.y:  # on monte
                y_temp -= self.current_speed
                if y_temp <= cible_courante[1]:
                    # on reajuste si le mob depasse ou atteint sa cible
                    depassement = cible_courante[1] - y_temp
                    self.y = cible_courante[1]
                    self.x += depassement
                    self.incremente_cible()
                else:
                    self.y -= self.current_speed

            elif cible_courante[1] > self.y:  # on descend
                y_temp += self.current_speed
                if y_temp >= cible_courante[1]:
                    depassement = y_temp - cible_courante[1]
                    self.y = cible_courante[1]
                    self.x += depassement
                    self.incremente_cible()
                else:
                    self.y += self.current_speed

        elif self.y == cible_courante[1]:  # on move suivant axe x
            x_temp += self.current_speed
            if x_temp >= cible_courante[0]:
                depassement = x_temp - cible_courante[0]
                if cible_suivante is not None:
                    if cible_suivante[1] < self.y:
                        self.y -= depassement
                    else:
                        self.y += depassement
                self.x = cible_courante[0]
                self.incremente_cible()
            else:
                self.x += self.current_speed

    def incremente_cible(self):
        if self.index_cible_courante == len(self.itineraire) - 1:  # on a atteint la derniere cible
            self.parent.creep_dies(self)
            self.parent.cegep_perd_un_point()
            self.parent.parent.get_vue().vue_ui.affiche_message("Des grévistes sont entré dans le Cégep !!")
        else:
            self.index_cible_courante += 1
