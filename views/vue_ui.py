# -*- coding: utf-8 -*-

from tkinter import *


class VueUI:
    def __init__(self, vue_main, y_offset):
        self.parent = vue_main
        self.yOffset = y_offset

        # init labels
        goLabelTxt = "Prochaine vague de grévistes"
        pauseLabelTxt = "Pause"
        placerTourLabelTxt = "Placer un gardien"
        self.score_label_txt = "Score: "
        self.hp_label_txt = "Étudiants en classe: "
        self.gold_label_txt = "Carrés rouges: "
        self.vague_label_txt = "Niveau: "
        self.message_label_txt = ""
        self.message_var = StringVar()
        self.score_var = StringVar()
        self.hp_var = StringVar()
        self.gold_var = StringVar()
        self.vague_var = StringVar()
        self.var_db = {"message": self.message_var,
                       "vague": self.vague_var,
                       "hp": self.hp_var,
                       "gold": self.gold_var,
                       "score": self.score_var}
        self.update_menu()

        self.display_ui_elements()
        self.affiche_message("Clic gauche - Placez un gardien(40CR) pour protéger le Cégep des grévistes")
        self.update_menu()

    def display_ui_elements(self):
        for id, buttonData in self.parent.get_game().uidb.items():
            if id != "pause":
                if "text" in buttonData:
                    self.create_text(buttonData["coords"], font=buttonData["font"], text=buttonData["text"],
                                     fill="#ccc", activefill='#fff')
                if "var" in buttonData:
                    self.create_text(buttonData["coords"], font=buttonData["font"], text=self.var_db[id].get(),
                                     fill="#ccc", activefill='#fff')

    # Update le menu en mettant a jour la valeur des strings des labels
    def update_menu(self):
        self.parent.canevas.delete("layer 99")
        self.display_ui_elements()

        self.message_var.set(self.message_label_txt)
        self.score_var.set(self.score_label_txt + str(self.parent.get_game().score))
        self.hp_var.set(self.hp_label_txt + str(self.parent.get_game().hp))
        self.gold_var.set(self.gold_label_txt + str(self.parent.get_game().gold))
        self.vague_var.set(self.vague_label_txt + str(self.parent.get_game().niveau))

    # ------ Buttons
    def create_rectangle(self, x1, y1, x2, y2):
        self.parent.add_to_layer(99, self.parent.canevas.create_rectangle,
                                 (x1, y1 + self.yOffset, x2, y2 + self.yOffset))

    def create_text(self, center_coords, **kwargs):
        c_list = list(center_coords)
        c_list[1] += self.yOffset
        center_coords = tuple(c_list)
        self.parent.add_to_layer(99, self.parent.canevas.create_text, center_coords, **kwargs)

    def affiche_message(self, message):
        self.message_label_txt = message
