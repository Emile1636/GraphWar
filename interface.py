import customtkinter as ctk
from accueil import Accueil
from formulaire import Formulaire
from jeu import Jeu
from joueur import Joueur

class Interface(ctk.CTkFrame):  # Définition de l'écran d'accueil
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.setup()

    def setup(self):
        # Initialisation et configuration du frame
        color_back = "#121D22" # 121D22
        self.configure(fg_color=color_back) # Couleur de la fenetre
        self.main_frame = ctk.CTkFrame(self, fg_color=color_back) # Couleur du frame
        self.main_frame.grid(sticky="nsew") # Frame format grid (row=1, column=0, pady=30, padx=20,)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center") # Centrer sur le fenetre, entre 0.0 (gauche) et 1.0 (droite) 

        # Création des "pages" en évitant une initialisation circulaire
        self.accueil = Accueil(self.master, self.main_frame, self.master)
        self.formulaire = Formulaire(self.master, self.main_frame, self.accueil)
        self.jeu = Jeu(self.master, self.main_frame, self.accueil)
        self.joueur = Joueur(self.accueil, self.jeu.get_obstacles())
        self.accueil.set_formulaire(self.formulaire)
        self.accueil.set_jeu(self.jeu)
        self.accueil.set_nom_joueur(self.joueur.get_nom_joueur())
        self.accueil.afficher_accueil() # Lancer l'accueil par défaut