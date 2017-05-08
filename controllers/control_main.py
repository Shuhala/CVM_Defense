# -*- coding: utf-8 -*-

from controllers.vue_main import Vue

from models import Partie


class Controleur:
    def __init__(self):
        self.partie = Partie(self)
        self.vue = Vue(self)
        # f = 40ms => environ 25 images/seconde: minimum acceptable
        # f = 20ms => 50fps
        self.frequence_cycles = 40  # temps entre 2 cycles en ms
        self.jouer()
        self.vue.root.mainloop()

    def jouer(self):
        self.partie.update_game()
        self.vue.update_game()
        self.vue.root.after(self.frequence_cycles, self.jouer)  # Durée d'un cycle en milliseconde

