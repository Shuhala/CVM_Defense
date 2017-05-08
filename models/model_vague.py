# -*- coding: utf-8 -*-

from models.model_creep import Creep


class Vague:
    def __init__(self, partie, layout_vague):
        self.parent = partie
        # layout_vague est un OrderedDict
        # sa derniere valeur est la frequence de pop  des creeps
        self.pop_frequency = layout_vague['pop_frequency']
        self.parent.frequence_de_pop_courante = self.pop_frequency
        del layout_vague['pop_frequency']
        # creep_list est une liste de listes contenant chacune:
        # - int type de mob: voir les listes de Andy
        # - int nombre de mobs de ce type
        self.creep_list = []
        self.invoke_creeps(layout_vague)

    def invoke_creeps(self, layout_vague):
        for creep_type, creep_count in layout_vague.items():  # pour chaque type de mob de cette vague
            for i in range(creep_count):
                self.creep_list.append(Creep(self, creep_type))

    def get_sentier(self):
        return self.parent.get_sentier()

    def creep_dies(self, c):
        self.parent.creep_dies(c)

    def is_empty(self):
        return len(self.creep_list) <= 0

    def is_not_empty(self):
        return len(self.creep_list) > 0

    def get_next_creep(self):
        return self.creep_list.pop(0)

    def get_creep_db(self):
        return self.parent.creep_database

    def cegep_perd_un_point(self):
        self.parent.cegep_perd_un_point()
