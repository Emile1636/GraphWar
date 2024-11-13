import pandas as pd
import numpy as np
import os
import sys

class Obstacles: 
    def __init__(self):
        # Chein d'acces vers le fichier .csv dans l'application .exe crée avec PyInstaller 
        if getattr(sys, 'frozen', False):
            # Si le script est compilé par PyInstaller
            base_path = sys._MEIPASS
        else:
            # Sinon, le script est exécuté directement
            base_path = os.path.dirname(__file__)

        # Charge le fichier CSV en utilisant le chemin d'accès correct
        self.villes_data = pd.read_csv(os.path.join(base_path, 'uscities.csv'))

        # Supprimer les colonnes inutiles
        colonnes_a_supprimer = ['source', 'military', 'incorporated', 'zips', 'id', 'ranking', 'timezone', 'county_fips']
        self.villes_data = self.villes_data.drop(columns=colonnes_a_supprimer)
        
    def generer_obstacles(self):
        # Choisir un État aléatoire
        etat_choisi = self.villes_data['state_name'].sample(n=1).iloc[0] # .sample retourn une liste de n=1 État et .iloc y accède
        # Filtrer les villes de cet État
        villes_etat = self.villes_data[self.villes_data['state_name'] == etat_choisi]
        # Vérifier si suffisamment de villes sont disponibles
        if len(villes_etat) < 25:
            return self.generer_obstacles() # On recommence

        # Sélectionner un nombre de villes
        nb_obstacles = np.random.randint(25)
        villes_choisies = villes_etat.sample(n=nb_obstacles)

        # Trier les villes choisies par population (ordre décroissan t)
        villes_choisies = villes_choisies.sort_values(by='population', ascending=False).reset_index(drop=True)

        # Déterminer les bornes min/max pour la latitude et longitude
        lat_min, lat_max = villes_etat['lat'].min(), villes_etat['lat'].max()
        lng_min, lng_max = villes_etat['lng'].min(), villes_etat['lng'].max()

        obstacles = []
        taille_min, taille_max = 5, 20  # Définir la plage de tailles
        distance_min = 15  # Distance minimale entre les obstacles pour éviter (trop) de chevauchement
        marge_x, marge_y = 30, 30  # Marges pour éviter les bordures

        for index, ville in villes_choisies.iterrows(): # itération sur les villes
            if len(obstacles) < 15:
               # Ajuster la latitude et la longitude pour qu'elles respectent la marge
                lat_ajustee = np.interp(ville['lat'], (lat_min, lat_max), (marge_x, 380 - marge_x))
                lng_ajustee = np.interp(ville['lng'], (lng_min, lng_max), (marge_y, 200 - marge_y))
                
                # Calculer la taille de l'obstacle selon la position dans la liste triée
                taille_obstacle = np.interp(index, [0, len(villes_choisies) - 1], [taille_max, taille_min])

                # Vérifier la distance avec les obstacles existants
                valid_position = True
                for x, y, _ in obstacles:
                    distance = np.sqrt((lat_ajustee - x) ** 2 + (lng_ajustee - y) ** 2) # Calcul de distance
                    if distance < (taille_obstacle + distance_min):
                        valid_position = False
                        break
                    # Réessayer la position si elle est trop proche d'un autre obstacle

                if valid_position:
                    obstacles.append((lat_ajustee, lng_ajustee, taille_obstacle)) # Ajouter l'obstacle à la liste
                else:
                    continue  # Passer à la ville suivante si trop proche
            else : break
        return obstacles