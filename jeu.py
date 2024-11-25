import customtkinter as ctk  
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importation pour intégrer Matplotlib avec tkinter
from joueur import Joueur  
from tir import Tir  
from traitementCSV import Obstacles
from matplotlib.patches import Circle
import json
import os

class Jeu(ctk.CTkFrame):
    def __init__(self, master, main_frame, accueil):
        super().__init__(master)
        self.master = master
        self.main_frame = main_frame
        self.accueil = accueil
        self.bool = True
        # Crée un frame pour le graphique
        self.plot_frame = ctk.CTkFrame(self)
        self.creation_jeu()

    def creation_jeu(self):
        # Création de la figure et des axes pour le tracé
        self.fig, self.ax = plt.subplots()   
        # Retirer les bordures (spines) du graphique
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        # Créer les obstacles, joueur, tir
        self.obstacles_instance = Obstacles() 
        self.obstacles = self.obstacles_instance.generer_obstacles()  
        self.joueur = Joueur(self, self.obstacles)
        self.tir = Tir(self)
        # Suivre les pointages et le temps
        self.score, self.obstacles_touches, self.ratio = 0, 0, 0
        self.time_left = 100
        self.is_flashing = False 

        # Créer les boutons et labels
        self.function_types = {
            "Linear": "x",
            "Quadratic": "0.01*x**2",
            "Exponential": "np.exp(x*0.1)",
            "Sinus": "np.sin(x*0.1)*10",
            "Cosine": "np.cos(x)",
        }
        # Première ligne
        self.score_label = ctk.CTkLabel(self.main_frame, text=f"Score: {self.score}", width=150, height=40, corner_radius=15, fg_color="#16a085", font=("Arial", 18, "bold"), text_color="#F8F6F6")
        self.func_selector = ctk.CTkComboBox(self.main_frame, values=list(self.function_types.keys()), command=self.tir.plot_selected_function, width=220, height=50, corner_radius=25, fg_color="white", text_color="black", font=("Arial", 18, "bold"))
        self.entry_func = ctk.CTkEntry(self.main_frame, placeholder_text="Enter a function", width=220, height=50, corner_radius=25, fg_color="white", text_color="black", font=("Arial", 18, "bold"))
        self.timer_label = ctk.CTkLabel(self.main_frame, text=f"Timer : {self.time_left}", width=150, height=40, corner_radius=15, fg_color="#16a085", font=("Arial", 18, "bold"), text_color="#F8F6F6")
        # Deuxieme ligne
        self.obstacles_label = ctk.CTkLabel(self.main_frame, text=f"Precision: {self.obstacles_touches:.0f}%", width=150, height=40, corner_radius=15, fg_color="#16a085", font=("Arial", 18, "bold"), text_color="#F8F6F6")
        self.reset_map_button = ctk.CTkButton(self.main_frame, text="Skip map", command=lambda: [self.tir.reset_plot(), setattr(self, 'time_left', self.time_left - 10)], width=220, height=50, corner_radius=25, fg_color="#f39c12", hover_color="#d57e2b", font=("Arial", 18, "bold"))
        self.plot_button = ctk.CTkButton(self.main_frame, text="Plot function", command=self.tir.plot_function, width=220, height=50, corner_radius=25, fg_color="#ff6347", hover_color="#d93c3a", font=("Arial", 18, "bold"))
        self.reset_button = ctk.CTkButton(self.main_frame, text="Reset", command=self.reset_all, width=150, height=40, corner_radius=15, fg_color="#16a085", hover_color="#12876f", font=("Arial", 18, "bold"))
        # Quatrième
        self.bouton_chat = ctk.CTkButton(self.main_frame, text="Ask question", command=lambda:[self.set_bool(False), self.set_score_joueur(self.score), self.masquer_jeu(), self.accueil.chat.afficher_chat()], corner_radius=17, width=200, height=40, fg_color="#16a085", hover_color="#12876f", font=("Arial", 20, "bold"))
        self.bouton_retour = ctk.CTkButton(self.main_frame, text="Back", command=lambda:[self.set_bool(False), self.set_score_joueur(self.score), self.masquer_jeu(), self.retour_accueil()], corner_radius=16, width=150, height=37, fg_color="#e74c3c", hover_color="#d93c3a", font=("Arial", 20, "bold"))
        
    def lancer_jeu(self):
        self.time_left = 101
        self.ratio = 0
        self.set_score(0)
        self.update_score()
        self.update_obstacles_touches()
        self.set_bool(True)
        self.update_timer() # Partir le timer
        self.afficher_jeu()

    def afficher_jeu(self):
        # Disposition des éléments sur plusieurs lignes 

        # Première ligne : Score, selectionner fct, entrer fct, timer
        self.score_label.grid(row=0, column=0, padx=(265, 10), pady=10)
        self.func_selector.grid(row=0, column=1, padx=10, pady=10)
        self.entry_func.grid(row=0, column=2, padx=10, pady=10)
        self.entry_func.configure(placeholder_text="Enter a function")
        self.timer_label.grid(row=0, column=3, padx=(10, 266), pady=10)

        # Deuxième ligne : Précision(obstacles), tracer, nouvelle map, reset
        self.obstacles_label.grid(row=1, column=0, padx=(265, 10), pady=10)
        self.reset_map_button.grid(row=1, column=2, padx=10, pady=10)
        self.plot_button.grid(row=1, column=1, padx=10, pady=10)
        self.reset_button.grid(row=1, column=3, padx=(10, 265), pady=10)
        # Configurez les lignes pour ne pas affecter les lignes 1 et 2
        self.main_frame.grid_rowconfigure(0, weight=0)  # Pas de redimensionnement pour la première ligne
        self.main_frame.grid_rowconfigure(1, weight=0)  # Pas de redimensionnement pour la deuxième ligne
        self.main_frame.grid_rowconfigure(2, weight=1)  # Permet à la troisième ligne de se redimensionner

        # Troisième ligne : Le canvas du graphique
        self.canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
        # Définissez une taille maximale pour le canvas (optionnel)
        max_width = 1350  
        max_height = 650
        self.canvas.get_tk_widget().config(width=max_width, height=max_height)
        # Placez le canvas sous les boutons et étirez-le pour occuper toute la largeur de la fenêtre
        self.canvas.get_tk_widget().grid(row=2, columnspan=4, sticky="ew", padx=10, pady=10)
        self.plot_obstacles_and_goal() # Tracer les obstacles et la cible

        # Quatrième ligne 
        self.bouton_chat.grid(row=3, columnspan=4, padx=10, pady=5)
        self.bouton_retour.grid(row=4, columnspan=4, padx=10, pady=5)
        self.tir.reset_plot()

    def masquer_jeu(self):
        self.legend.set_visible(False)
        self.score_label.grid_remove()
        self.func_selector.grid_remove()
        self.entry_func.delete(0, "end")
        self.entry_func.grid_remove()
        self.timer_label.grid_remove()
        self.obstacles_label.grid_remove()
        self.reset_map_button.grid_remove()
        self.plot_button.grid_remove()
        self.reset_button.grid_remove()
        self.canvas.get_tk_widget().grid_remove()
        self.bouton_retour.grid_remove()
        self.bouton_chat.grid_remove()

    def retour_accueil(self):
        # Retour accueil
        if self.accueil.get_nom_joueur() != "Player":
            self.accueil.afficher_accueil(True)
        else :
            self.accueil.afficher_accueil(False)

    def plot_obstacles_and_goal(self):
        for obstacle in self.joueur.obstacles:  # Itération sur les obstacles
            x, y, r = obstacle  # Décomposition du tuple
            # Création de plusieurs cercles pour l'effet de lueur
            for i in range(2):
                glow_radius = r + 0.2 * i  # Rayons croissants
                glow_alpha = 0.05 + 0.05 * i  # Alpha décroissant pour l'effet de lueur
                glow_circle = Circle((x, y), glow_radius, color='red', alpha=glow_alpha)  # Cercle de lueur
                self.ax.add_patch(glow_circle)  # Ajout du cercle au tracé

            circle = Circle((x, y), r, color='red', alpha=0.5)  # Crée un cercle avec les coordonnées et le rayon
            self.ax.add_patch(circle)  # Ajout du cercle au tracé

        # Tracé du joueur et de la cible
        self.ax.plot(self.joueur.joueur_position[0], self.joueur.joueur_position[1], 'bv', markersize=10, label=self.accueil.get_nom_joueur())
        self.ax.plot(self.joueur.cible_position[0], self.joueur.cible_position[1], 'go', markersize=10, label='Target')
        # Définition des limites des axes
        self.ax.set_xlim(0, 360)  
        self.ax.set_ylim(0, 200)  
        self.ax.set_aspect('equal', 'box')  # Assurer un aspect égal pour le tracé
        # Légende
        self.legend = self.ax.legend(loc="upper left", prop = { "size": 6 }, markerscale=0.6, bbox_to_anchor=(1, 1))
        self.legend.get_frame().set_facecolor("#121D22")  # Couleur de fond de la légende 
        self.legend.get_frame().set_edgecolor("#121D22")  # Couleur de la bordure de la légende 
        self.ax.set_facecolor("#121D22") # Interieur
        self.fig.set_facecolor("#121D22") # Exterieur
        for text in self.legend.get_texts():
            text.set_color("white")
        self.ax.set_xticks([]) # Supprimer les graduations
        self.ax.set_yticks([])
        self.canvas.draw()

    def get_obstacles(self):
        return self.obstacles
    
    def update_score(self):
        self.score_label.configure(text=f"Score: {self.score}") 
        
    def update_obstacles_touches(self):
        if self.get_score_joueur() != False:
            self.obstacles_label.configure(text=f"Record: {self.get_score_joueur()}")
        else:
            self.obstacles_label.configure(text=f"Precision: {self.ratio:.0f}%")
        
    def increment_score(self):
        if self.time_left > 0:
            self.score += 1
        self.ratio = (self.score  / (self.obstacles_touches + self.score)) * 100
        self.update_obstacles_touches()
        self.update_score()
        self.time_left += 10
        
    def increment_obstacles_touches(self):
        self.obstacles_touches += 1
        self.ratio = (self.score  / (self.obstacles_touches + self.score)) * 100
        self.update_obstacles_touches()

    def update_timer(self):
        if self.time_left <= 0:
            self.timer_label.configure(text_color="#F8F6F6")  # Couleur normale
            self.is_flashing = not self.is_flashing
            self.timer_label.configure(text="Time's up!")
            self.set_score_joueur(self.score)
            self.bool = True
            return
        
        self.time_left -= 1
        self.timer_label.configure(text=f"Timer : {self.time_left}")  # Mettre à jour le texte du timer
        # Clignotement : alterner la couleur à chaque seconde
        if self.time_left <= 29:
            if self.is_flashing:
                self.timer_label.configure(text_color="#F8F6F6")  # Couleur normale
            else:
                self.timer_label.configure(text_color="red")  # Couleur de clignotement
            self.is_flashing = not self.is_flashing  # Alterner l'état du clignotement
        # Réappeler la fonction après 1000ms (1 seconde)
        if self.get_bool() is True:
            self.master.after(1000, lambda: self.update_timer())

    def reset_all(self):
        self.bool = False
        self.obstacles_touches = 0
        self.ratio = 0
        self.score = 0
        self.timer_label.configure(text_color="#F8F6F6")
        self.time_left = 101
        self.tir.reset_plot()
        self.update_timer()
        self.update_score()
        self.update_obstacles_touches()
        self.bool = True

    def set_score(self, score):
        self.score = score

    def set_score_joueur(self, score):
        if not os.path.exists("utilisateurs.json"):
            utilisateurs = {self.accueil.get_nom_joueur(): {"password": "default_password", "score": score}}
            with open("utilisateurs.json", "w") as f:
                json.dump(utilisateurs, f, indent=4)
            return

        with open("utilisateurs.json", "r") as f:
            utilisateurs = json.load(f)

        joueur_nom = self.accueil.get_nom_joueur()
        if joueur_nom in utilisateurs:
            if 'score' not in utilisateurs[joueur_nom] or score > utilisateurs[joueur_nom]['score']:
                utilisateurs[joueur_nom]['score'] = score
        # Uptatde fichier
        with open("utilisateurs.json", "w") as f:
            json.dump(utilisateurs, f, indent=4)

    def get_score_joueur(self):
        nom = self.accueil.get_nom_joueur()
        if not os.path.exists("utilisateurs.json"):
            return 
        
        with open("utilisateurs.json", "r") as f:
            utilisateurs = json.load(f)

        if nom in utilisateurs:
            if 'score' not in utilisateurs[nom]:
                utilisateurs[nom]['score'] = 0
                return utilisateurs[nom]['score']
            else:
                return utilisateurs[nom]['score']
        else:
            return False
             
    def set_bool(self, bool):
        self.bool = bool

    def get_bool(self):
        return self.bool
