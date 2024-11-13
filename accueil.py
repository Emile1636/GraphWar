import customtkinter as ctk

class Accueil:
    def __init__(self, master, main_frame, app):
        self.master = master
        self.main_frame = main_frame
        self.nom_joueur = ""
        self.bouton_deconnexion_exist = False
        self.app = app  # Référence à l'instance de Application

    def set_formulaire(self, formulaire):
        self.formulaire = formulaire

    def set_nom_joueur(self, pseudo):
        self.nom_joueur = pseudo

    def set_jeu(self, jeu):
        self.jeu = jeu

    def get_nom_joueur(self):
        if self.nom_joueur == "":
            return "Player"
        else:
            return self.nom_joueur

    def afficher_accueil(self):
        # Titre "Graph" et "War"
        self.label_graph = ctk.CTkLabel(self.main_frame, text="Graph", font=("Arial", 180, "bold"), text_color="#16a085")
        self.label_graph.grid(row=0, column=0, columnspan=2, padx=(0, 400), pady=(0, 100))
        self.label_war = ctk.CTkLabel(self.main_frame, text="War", font=("Arial", 180, "bold"), text_color="#d57e2b")
        self.label_war.grid(row=0, column=1, columnspan=2, padx=(10, 0), pady=(0, 100))

        # Boutons: Jouer, Connexion, Inscription, Déconnexion
        self.bouton_jouer = ctk.CTkButton(self.main_frame, text="Play", command=self.lancer_jeu, width=300, height=70, corner_radius=30, fg_color="#ff6347", hover_color="#d93c3a", font=("Arial", 34, "bold"))
        self.bouton_deconnexion = ctk.CTkButton(self.main_frame, text="Log out", command=lambda:[self.formulaire.set_nom_joueur(""), self.masquer_accueil(), self.afficher_accueil()], width=250, height=60, corner_radius=25, fg_color="#48C9B0", hover_color="#16a085", font=("Arial", 24, "bold"))
        self.bouton_connexion = ctk.CTkButton(self.main_frame, text="Login", command=self.lancer_connexion, width=250, height=60, corner_radius=25, fg_color="#48C9B0", hover_color="#16a085", font=("Arial", 24, "bold"))
        self.bouton_inscription = ctk.CTkButton(self.main_frame, text="Sign in", command=self.lancer_inscription, width=250, height=60, corner_radius=25, fg_color="#f39c12", hover_color="#d57e2b", font=("Arial", 24, "bold"))
        self.bouton_quitter = ctk.CTkButton(self.main_frame, text="Quit", command=self.app.quit_app, width=250, height=60, corner_radius=25, fg_color="#34495e",  font=("Arial", 24, "bold"))
        # Placer sur la grille
        if self.formulaire.get_nom_joueur() != "":
            self.bouton_deconnexion_exist = True
            self.bouton_jouer.grid(row=1, column=0, columnspan=2, pady=15)
            self.bouton_deconnexion.grid(row=2, column=0, columnspan=2, pady=15)
            self.bouton_quitter.grid(row=3, column=0, columnspan=2, pady=15)
        else:
            self.bouton_deconnexion_exist = False
            self.bouton_jouer.grid(row=1, column=0, columnspan=2, pady=15)
            self.bouton_connexion.grid(row=2, column=0, columnspan=2, pady=15)
            self.bouton_inscription.grid(row=3, column=0, columnspan=2, pady=15)
            self.bouton_quitter.grid(row=4, column=0, columnspan=2, pady=15)

    def masquer_accueil(self):
        self.label_graph.grid_remove()
        self.label_war.grid_remove()
        self.label_graph.grid_remove()
        self.label_war.grid_remove()
        self.bouton_jouer.grid_remove()
        self.bouton_connexion.grid_remove()
        self.bouton_inscription.grid_remove()
        self.bouton_quitter.grid_remove()
        if self.bouton_deconnexion_exist:
            self.bouton_deconnexion.grid_remove()

    def lancer_jeu(self):
        self.masquer_accueil()
        self.jeu.lancer_jeu()

    def lancer_connexion(self):
        self.masquer_accueil()
        self.formulaire.afficher_connexion()

    def lancer_inscription(self):
        self.masquer_accueil()
        self.formulaire.afficher_inscription()
