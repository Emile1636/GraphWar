import numpy as np  # Importation de NumPy pour les calculs mathématiques

class Joueur:  # Définition de la classe Joueur
    def __init__(self, accueil, obstacles):
        self.accueil = accueil
        self.obstacles = obstacles
        self.nom_joueur = ""
        self.reference = (0, 0) # Reference au dernier point créé, évite alors de créé un point sur le dernier existant
        self.joueur_position = self.generer_position_valide_point() 
        self.cible_position = self.generer_position_valide_point()

    def set_nom_joueur(self, pseudo):
        self.nom_joueur = pseudo

    def get_nom_joueur(self):
        return self.nom_joueur

    def generer_position_valide_point(self): # Méthode pour générer la position du joueur, retourne un position valide
        while True: # Jusqu'à obtenir une position valide
            xpoint = np.random.randint(10, 340)
            ypoint = np.random.randint(10, 180)
            is_valide = True 
            for (xobstacle, yobstacle, robstacle) in self.obstacles: # Vérifier pour chaque obstacle
                # On calcul la distance entre le point et l'obstacle
                odistance = np.sqrt((xpoint-xobstacle)**2 + (ypoint - yobstacle)**2)
                if odistance < (robstacle + 10): 
                    is_valide = False 
                # On calcul la distance entre le point et le point de reference
                pdistance = np.sqrt((xpoint-self.reference[0])**2 + (ypoint - self.reference[1])**2) 
                if pdistance < 10: 
                    is_valide = False 
            if is_valide :
                self.reference = (xpoint, ypoint) # Le point de reference devient le point
                return (xpoint, ypoint)
            