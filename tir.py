import numpy as np  
from joueur import Joueur
import tkinter as tk

# Fonction pour vérifier si un point est dans un cercle
def touche_au_cercle(x, y, cercle_x, cercle_y, rayon):
    return (x - cercle_x)**2 + (y - cercle_y)**2 <= rayon**2

class Tir: 
    def __init__(self, accueil): # Constructeur qui prend en paramètre l'interface graphique
        self.accueil = accueil 
        self.obstacles = accueil.obstacles  # Initialiser les obstacles

    def plot_function(self):  
        equation = self.accueil.entry_func.get()  # Récupère la fonction entrée par l'utilisateur
        if not equation:  # Vérifie si la fonction est vide
            print("Please enter valide function")
            self.accueil.entry_func.delete(0, "end")
            self.accueil.entry_func.configure(placeholder_text="* Invalid", placeholder_text_color="#F14156", font=("Arial", 18, "bold"))
            return
    
        # Sécurité pour éviter les transaltion verticale ------------------------- A revoir pour les - (ex : -0.1*x)
        nb_plus, nb_moins, nb_x, no = 0, 0, 0, 0 
        caract_special = ['!', '@', '#', '$', '%', '?', '&', '_', '=', ';', '<', '>', ',', ':', '¨', '^', '~', '»', '«']
        for l in caract_special:
            if l in equation:
                self.accueil.entry_func.delete(0, "end")
                self.accueil.entry_func.configure(placeholder_text="* Invalid", placeholder_text_color="#F14156", font=("Arial", 18, "bold"))
                return
        if '+' in equation or '-' in equation:
            for i in equation:
                if i == '+' : nb_plus += 1
                if i == 'x' : nb_x += 1
                # if i == '-' and equation[no+1] != 'x': nb_moins += 1 (-0.5*x)
                no += 1
            if nb_plus >= nb_x or nb_moins >= nb_x:
                print("La fonction ne peut pas être translatée verticalement.")
                self.accueil.entry_func.delete(0, "end")
                self.accueil.entry_func.configure(placeholder_text="* Invalid", placeholder_text_color="#F14156", font=("Arial", 18, "bold"))
                return
        
        # Position du joueur et de la cible
        joueur_pos = self.accueil.joueur.joueur_position 
        cible_pos = self.accueil.joueur.cible_position  
        # Convertir en coordonnées
        x_joueur, y_joueur = joueur_pos 
        x_cible, y_cible = cible_pos

        # Générer des valeurs x entre les limites du plan (x = [0, 360], y = [0, 200])
        x_fct = np.linspace(0, 360, 2000)
        
        # Évaluer l'équation pour obtenir y
        try:
            y_fct = eval(equation, {"x": x_fct, "np": np})
        except Exception as e:
            print(f"Error in equation : {e}")
            return
        
        # Faire une translation horizontale et vertical de la fonction afin de la faire commencer (0,0) au joueur (x_joueur, y_joueur)
        x_fct = x_fct + x_joueur
        y_fct = y_fct + y_joueur 

        # Appliquer une réflexion si le joueur est à droite de la cible
        if x_joueur > x_cible:
            # Calcul de la réflexion : inversion des valeurs x autour de x_joueur
            x_fct = 2 * x_joueur - x_fct

        # Initialiser les listes pour la fonction qui sera afficher
        trajectoire_x = []
        trajectoire_y = []
        # Stocker les coordonnées des collisons
        collision_x = None 
        collision_y = None
        cible_touchee = False

        # Vérification des collisions
        for i in range(len(x_fct)):
            # Vérifier la collision avec les obsatcles 
            collision = False
            for obstacle in self.obstacles:  # Itération sur les obstacles
                x, y, r = obstacle  # Décomposition de l'obsatcles
                if touche_au_cercle(x_fct[i], y_fct[i], x, y, r): # Attention : il faut considerer que les obstacles sont toujours aux coordonnées normales, mais que la fonction est translaté
                    print(f"Obstacle touché en : ({x_fct[i]:.2f}, {y_fct[i]:.2f})")
                    collision_x = x_fct[i]
                    collision_y = y_fct[i]
                    collision = True
                    self.accueil.increment_obstacles_touches()  # Incrémenter obstacles touchés
                    break 

            if collision:
                break  # Quitte la boucle principale si collision avec obstacle

            # Vérifier la collision avec la cible
            if touche_au_cercle(x_fct[i], y_fct[i], x_cible, y_cible, 5):
                print(f"Cible touchée en : ({x_fct[i]:.2f}, {y_fct[i]:.2f})") # Attention, comme pour les obstacles
                cible_touchee = True
                self.accueil.increment_score()  # Incrémenter le score
                break

            # Ajouter le point actuel à la trajectoire s'il n'y a pas eu de collision
            trajectoire_x.append(x_fct[i])
            trajectoire_y.append(y_fct[i])

        # Trajectoire
        self.accueil.ax.plot(trajectoire_x, trajectoire_y, label=f'{equation}') 

        # Effe de collision
        if collision_x is not None and collision_y is not None:
            self.accueil.ax.plot(collision_x, collision_y, 'ro', markersize=3)
    
        # Arranger le visuel
        self._finalize_plot()

        # Si la cible est touchée, ajoutez un délai, puis réinitialisez la scène
        if cible_touchee:
            self.cible_atteinte()  # Appelle la méthode pour gérer la réinitialisation après la cible atteinte
            
    def cible_atteinte(self):
        self.accueil.after(800, self.reset_plot)  # Attente de 1 secondes avant réinitialisation

    def reset_plot(self):
        self.accueil.ax.clear()
        # Générer de nouveaux obstacles et mettre à jour les obstacles dans l'instance Tir
        self.accueil.obstacles = self.accueil.obstacles_instance.generer_obstacles()
        self.obstacles = self.accueil.obstacles
        # Générer un nouveau joueur avec les nouveaux obstacles
        self.accueil.joueur = Joueur(self.accueil, self.accueil.obstacles)
        self.accueil.plot_obstacles_and_goal()
        # Tracer les obstacles et la cible
        self._finalize_plot()

    def plot_selected_function(self, choice): # Méthode pour tracer une fonction sélectionnée
        func_text = self.accueil.function_types.get(choice) # Récupère la fonction associée au choix
        self.accueil.entry_func.delete(0, tk.END) # Efface le champ de saisie
        self.accueil.entry_func.insert(0, func_text) # Insère la fonction sélectionnée dans le champ
        self.plot_function() # Appelle la méthode pour tracer la fonction

    def _finalize_plot(self):
        self.accueil.ax.set_xticks([])
        self.accueil.ax.set_yticks([])
        # Legend setup
        legend = self.accueil.ax.legend(loc="upper left", prop={"size": 6}, markerscale=0.6, bbox_to_anchor=(1, 1) )
        legend.get_frame().set_facecolor("#121D22") # Interieur
        legend.get_frame().set_edgecolor("#121D22") # Interieur
        for text in legend.get_texts():
            text.set_color("white")
        self.accueil.canvas.draw()
