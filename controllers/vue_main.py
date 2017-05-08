# -*- coding: utf-8 -*-

from tkinter import *

from views.vue_ui import VueUI
from settings import *


class Vue:
    def __init__(self, controller):

        self.parent = controller

        # init vars
        self._layers = []
        self.hauteur_ui = self.parent.partie.hauteur_ui
        self.menu_confirm_popup = None
        self.upgrade_popup = None
        self.intro_closed = False
        self.uiButtons = {}
        self.step = 20

        # init tk
        self.root = Tk()

        # init skins
        self.skinsmobs = {"mob1": PhotoImage(file=IMG_ROOT+'/mob1.png'), "mob2": PhotoImage(file=IMG_ROOT+'/mob2.png'),
                          "mob3": PhotoImage(file=IMG_ROOT+'/mob3.png'), "boss1": PhotoImage(file=IMG_ROOT+'/boss1.png'),
                          "boss2": PhotoImage(file=IMG_ROOT+'/boss2.png'),
                          "boss3": PhotoImage(file=IMG_ROOT+'/boss3.png'),
                          "andra": PhotoImage(file=IMG_ROOT+'/boss4.png')}
        self.intro = PhotoImage(file=IMG_ROOT+'/intro.png')
        self.fond = PhotoImage(file=IMG_ROOT+'/fond.png')
        self.arbre = PhotoImage(file=IMG_ROOT+'/arbre.png')
        self.cegep = PhotoImage(file=IMG_ROOT+'/cegep.png')
        self.border = PhotoImage(file=IMG_ROOT+'/border.png')
        self.grouptente = PhotoImage(file=IMG_ROOT+'/grouptente.png')
        self.tentejaune = PhotoImage(file=IMG_ROOT+'/tentejaune.png')
        self.imgsentier = PhotoImage(file=IMG_ROOT+'/chemin2.png')
        self.tour = {0: PhotoImage(file=IMG_ROOT+'/tour0.png'), 1: PhotoImage(file=IMG_ROOT+'/tour1.png'),
                     2: PhotoImage(file=IMG_ROOT+'/tour2.png'), 3: PhotoImage(file=IMG_ROOT+'/tour3.png'),
                     4: PhotoImage(file=IMG_ROOT+'/tour4.png')}
        self.proj = {0: PhotoImage(file=IMG_ROOT+'/projectile0.png'), 1: PhotoImage(file=IMG_ROOT+'/projectile1.png'),
                     2: PhotoImage(file=IMG_ROOT+'/projectile2.png'), 3: PhotoImage(file=IMG_ROOT+'/projectile3.png'),
                     4: PhotoImage(file=IMG_ROOT+'/projectile4.png')}
        self.shopFrame = PhotoImage(file=IMG_ROOT+'/shopFrame.png')

        self.gameover = PhotoImage(file=IMG_ROOT+'/gameover.png')
        self.winscreen = PhotoImage(file=IMG_ROOT+'/winscreen.png')
        self.blood = PhotoImage(file=IMG_ROOT+'/blood.png')
        self.slow = PhotoImage(file=IMG_ROOT+'/slow.png')

        self.introcanvas = Canvas(self.root, width=self.parent.partie.largeur_aire,
                                  height=self.parent.partie.hauteur_aire + self.hauteur_ui, bg="black")
        self.introcanvas.create_image(2, 2, image=self.intro, anchor=NW, tag="intro")
        self.introcanvas.pack()
        self.introcanvas.bind("<Button-1>", self.left_click_on_canevas)

    def update_game(self):
        if self.parent.partie.intro_closed:
            if not self.intro_closed:
                self.close_intro()
            self.draw_game()
            self.update_menu()

    def close_intro(self):
        self.canevas = Canvas(self.root, width=self.parent.partie.largeur_aire,
                              height=self.parent.partie.hauteur_aire + self.hauteur_ui, bg="black")
        self.add_to_layer(10, self.canevas.create_image, (2, 2), image=self.fond, anchor=NW)
        self.canevas.bind("<Button-1>", self.left_click_on_canevas)
        self.canevas.bind("<Button-3>", self.right_click_on_canevas)
        self.draw_path(self.parent.partie.get_sentier())

        # fond de l'UI
        self.add_to_layer(80, self.canevas.create_image, (2, self.parent.partie.hauteur_aire + 2), image=self.shopFrame,
                          anchor=NW)
        self.vue_ui = VueUI(self, self.parent.partie.hauteur_aire)

        # on enleve l'image d'intro et on affiche le jeu
        self.introcanvas.delete("intro")
        self.introcanvas.pack_forget()
        self.canevas.pack()
        self.intro_closed = True

    # click event
    def left_click_on_canevas(self, evt):
        self.parent.partie.check_event_left_click(evt.x, evt.y)

    # Si on right-click sur le canevas
    def right_click_on_canevas(self, evt):
        self.parent.partie.check_event_right_click(evt.x, evt.y)

    def show_message(self, message):
        self.vue_ui.message_label_txt = message

    def start_game(self, event):
        self.parent.partie.start()

    def pause_game(self, event):
        self.parent.partie.toggle_pause()

    # dessine les elements graphiques statiques
    def draw_path(self, path):
        for i in range(len(path) - 1):
            if i != len(path) - 1:
                if path[i][0] == path[i + 1][0]:  # mm colonne
                    if path[i][1] <= path[i + 1][1]:  # suivant plus bas
                        for j in range(path[i][1], path[i + 1][1], self.step):
                            self.add_to_layer(20, self.canevas.create_image, (path[i][0], j), image=self.imgsentier)
                    elif path[i][1] > path[i + 1][1]:  # suivant plus haut
                        for j in range(path[i + 1][1], path[i][1], self.step):
                            self.add_to_layer(20, self.canevas.create_image, (path[i][0], j), image=self.imgsentier)
                elif path[i][1] == path[i + 1][1]:
                    for j in range(path[i][0], path[i + 1][0], self.step):
                        self.add_to_layer(20, self.canevas.create_image, (j, path[i][1]), image=self.imgsentier)
            self.add_to_layer(20, self.canevas.create_image, (path[i][0], path[i][1]), image=self.imgsentier)

        self.add_to_layer(60, self.canevas.create_image, (2, 2), image=self.border, anchor=NW)
        self.add_to_layer(30, self.canevas.create_image, (path[0][0] + 25, path[0][1] - 50), image=self.grouptente)
        self.add_to_layer(30, self.canevas.create_image, (path[len(path) - 1][0] - 50, path[len(path) - 1][1] - 65),
                          image=self.cegep)
        self.add_to_layer(40, self.canevas.create_image, (path[0][0], path[0][1] - 3), image=self.tentejaune)
        self.draw_trees()

    def draw_trees(self):
        for tree in self.parent.partie.trees:
            self.add_to_layer(55, self.canevas.create_image, (tree[0] + 25, tree[1] - 20), image=self.arbre)

    # dessine les elements graphiques dynamiques
    def draw_game(self):
        self.canevas.delete("layer 50")
        self.canevas.delete("layer 51")
        self.canevas.delete("layer 95")
        self.canevas.delete("layer 59")
        self.canevas.delete("layer 49")
        for i in self.parent.partie.vague_en_marche:
            self.add_to_layer(50, self.canevas.create_image, (i.x, i.y), image=self.skinsmobs[i.skin])
            self.add_to_layer(51, self.canevas.create_text, (i.x, i.y + 25), text=str(i.points_vie), fill="yellow")
            if i.slow_duration > 0:
                self.add_to_layer(49, self.canevas.create_image, (i.x, i.y), image=self.slow)

        for i in self.parent.partie.liste_tour:
            self.add_to_layer(50, self.canevas.create_image, (i.x, i.y), image=self.tour[i.type_tour[7]])
            for j in i.projectiles:
                self.add_to_layer(95, self.canevas.create_image, (j.x, j.y), image=self.proj[i.type_tour[6]])
        for i in self.parent.partie.mort:
            self.add_to_layer(49, self.canevas.create_image, (i.x, i.y), image=self.blood)
        self.update_menu()

    def show_winning_screen(self):
        self.canevas.delete("layer 61")
        self.add_to_layer(61, self.canevas.create_image, (2, 2), image=self.winscreen, anchor=NW)

    def show_looser_screen(self):
        self.canevas.delete("layer 61")
        self.add_to_layer(61, self.canevas.create_image, (2, 2), image=self.gameover, anchor=NW)

    # menu gameplay
    def open_turret_popup(self, click_x, click_y):
        self.menu_confirm_popup = Frame(self.canevas, width=150, height=25)
        menu_confirm_label = Label(self.menu_confirm_popup, text="Placer la Tour ici ?", width=150, fg="black", bg="yellow")

        button_conf_tour = Button(self.menu_confirm_popup, width=150,
                                  command=lambda: self.parent.partie.placer_tour(click_x, click_y), text="Confirmer",
                                  fg="yellow", bg="red")

        menu_confirm_label.pack()
        button_conf_tour.pack()
        self.menu_confirm_popup.pack()

        self.canevas.create_window(click_x, click_y, window=self.menu_confirm_popup, width=150, height=45)
        self.canevas.pack()

    def close_turret_popup(self):
        self.menu_confirm_popup.destroy()

    def close_turret_upgrade_popup(self):
        self.upgrade_popup.destroy()

    # fonction qui génère les fenêtres pour les upgrades de tours
    def open_turret_upgrade_popup(self, click_x, click_y, tour_selected):
        self.upgrade_popup = Frame(self.canevas, width=150, height=150)
        self.menu_upgrade_label = Label(self.upgrade_popup, text="Votre Upgrade : ", width=150, fg="black", bg="yellow")

        button_lacrymogenes = Button(self.upgrade_popup, width=150,
                                     command=lambda: self.parent.partie.upgrade_tour("Gaz Lacrymogènes", tour_selected),
                                     text="Gaz Lacrymogènes", fg="yellow", bg="red")
        button_range = Button(self.upgrade_popup, width=150,
                              command=lambda: self.parent.partie.upgrade_tour("Portée", tour_selected), text="Portée",
                              fg="yellow", bg="red")
        button_damage = Button(self.upgrade_popup, width=150,
                               command=lambda: self.parent.partie.upgrade_tour("Dommages", tour_selected), text="Dommages",
                               fg="yellow", bg="red")
        button_annuler = Button(self.upgrade_popup, width=150, command=self.close_turret_upgrade_popup, text="Annuler",
                                fg="yellow", bg="black")

        # desactive les upgrades de tour interdits : on ne peut qu'upgrader une seule caractéristique par tour
        if tour_selected.type_tour[7] == 1:
            button_range.configure(state=DISABLED, disabledforeground="grey")
            button_damage.configure(state=DISABLED, disabledforeground="grey")

        if tour_selected.type_tour[7] == 2:
            button_lacrymogenes.configure(state=DISABLED, disabledforeground="grey")
            button_damage.configure(state=DISABLED, disabledforeground="grey")

        if tour_selected.type_tour[7] == 3:
            button_lacrymogenes.configure(state=DISABLED, disabledforeground="grey")
            button_range.configure(state=DISABLED, disabledforeground="grey")

        # On pack les boutons et label dans le frame avant de packer la fenêtre
        self.menu_upgrade_label.pack()
        button_lacrymogenes.pack()
        button_range.pack()
        button_damage.pack()
        button_annuler.pack()

        # On crée la fenêtre contenant le frame upgradePopup et on pack le tout
        print(click_x, click_y)
        self.canevas.create_window(click_x, click_y, window=self.upgrade_popup, width=150, height=125)
        self.canevas.pack()

    # utils
    def get_game(self):
        return self.parent.partie

    def update_menu(self):
        self.vue_ui.update_menu()

    # les deux methodes ci dessous servent a la gestion des layers
    def add_to_layer(self, layer, command, coords, **kwargs):
        layer_tag = "layer %s" % layer
        if layer_tag not in self._layers: self._layers.append(layer_tag)
        tags = kwargs.setdefault("tags", [])
        tags.append(layer_tag)
        item_id = command(coords, **kwargs)
        self.adjust_layers()
        return item_id

    def adjust_layers(self):
        for layer in sorted(self._layers):
            self.canevas.lift(layer)
