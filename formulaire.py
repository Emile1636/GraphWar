import customtkinter as ctk
import json
import os
import bcrypt

class Formulaire(ctk.CTkFrame):
    def __init__(self, master, main_frame, accueil):
        super().__init__(master)  
        self.main_frame = main_frame
        self.accueil = accueil
        self.pseudo = ""
        self.creation_formaulaire()
    
    def creation_formaulaire(self):
        # Boutons de bascule Connexion/Inscription
        self.bouton_connexion = ctk.CTkButton(self.main_frame, text="Connexion", command=self.afficher_connexion,corner_radius=30, width=200, height=80, fg_color="#16a085", font=("Arial", 28, "bold"))
        self.bouton_inscription = ctk.CTkButton(self.main_frame, text="Inscription", command=self.afficher_inscription,corner_radius=30, width=200, height=80, fg_color="#34495e", font=("Arial", 28, "bold"))
        # Zones de texte pour le formulaire
        self.entry_pseudo = ctk.CTkEntry(self.main_frame, placeholder_text="Utilisateur", placeholder_text_color="#B0B0B0", width=440, height=80,corner_radius=25, fg_color="white", text_color="black", font=("Arial", 24, "bold"))
        self.entry_mdp = ctk.CTkEntry(self.main_frame, placeholder_text="Mot de passe", placeholder_text_color="#B0B0B0", show="*", width=440, height=80,corner_radius=25, fg_color="white", text_color="black", font=("Arial", 24, "bold"))
        self.entry_confirm_mdp = ctk.CTkEntry(self.main_frame, placeholder_text="Confirmer le mot de passe", placeholder_text_color="#B0B0B0", show="*", width=440, height=80,corner_radius=25, fg_color="white", text_color="black", font=("Arial", 24, "bold"))
        # Bouton de soumission et de retour
        self.bouton_valider = ctk.CTkButton(self.main_frame, text="Connexion", command=self.valider_formulaire, corner_radius=50, width=440, height=80, fg_color="#1abc9c", font=("Arial", 28, "bold"))
        self.bouton_retour = ctk.CTkButton(self.main_frame, text="Retour", command=lambda:[self.masquer_formulaire(), self.accueil.afficher_accueil()], corner_radius=30, width=300, height=60, fg_color="#e74c3c", hover_color="#d93c3a", font=("Arial", 24, "bold"))

    def afficher_connexion(self):
        # Positionner les éléments
        self.bouton_connexion.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.bouton_inscription.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.entry_pseudo.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.entry_mdp.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.bouton_valider.grid(row=4, column=0, columnspan=2, pady=40)
        self.bouton_retour.grid(row=5, column=0, columnspan=2, pady=1)
        self.entry_confirm_mdp.grid_remove() # masquer
        # Actualiser couleurs et texte selon la selecton
        self.entry_pseudo.delete(0, "end")
        self.entry_pseudo.configure(placeholder_text="Utilisateur", placeholder_text_color="#B0B0B0")
        self.entry_mdp.delete(0, "end")
        self.entry_mdp.configure(placeholder_text="Mot de passe", placeholder_text_color="#B0B0B0", show="*")
        self.bouton_valider.configure(text="Se connecter", hover_color="#16a085")
        self.bouton_connexion.configure(fg_color="#f39c12", hover_color="#d57e2b")
        self.bouton_inscription.configure(fg_color="#34495e")

    def afficher_inscription(self):
        # Positionner les éléments
        self.bouton_connexion.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.bouton_inscription.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.entry_pseudo.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.entry_mdp.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.entry_confirm_mdp.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.bouton_valider.grid(row=4, column=0, columnspan=2, pady=40)
        self.bouton_retour.grid(row=5, column=0, columnspan=2, pady=1)
        # Actualiser couleurs et texte selon la selecton
        self.entry_pseudo.delete(0, "end")
        self.entry_pseudo.configure(placeholder_text="Utilisateur", placeholder_text_color="#B0B0B0")
        self.entry_mdp.delete(0, "end")
        self.entry_mdp.configure(placeholder_text="Mot de passe", placeholder_text_color="#B0B0B0", show="*")
        self.entry_confirm_mdp.delete(0, "end")
        self.entry_confirm_mdp.configure(placeholder_text="Mot de passe", placeholder_text_color="#B0B0B0", show="*")
        self.bouton_valider.configure(text="S'inscrire", hover_color="#16a085")
        self.bouton_connexion.configure(fg_color="#34495e")
        self.bouton_inscription.configure(fg_color="#f39c12", hover_color="#d57e2b")

    def valider_formulaire(self):
        '''Gestion de la validation selon l'option sélectionné (connexion/inscription)'''
        # Éléments communs / Réccupération données saisit
        self.pseudo = self.entry_pseudo.get()
        self.mdp = self.entry_mdp.get()
        self.confirm_mdp = self.entry_confirm_mdp.get() if self.bouton_valider.cget("text") == "S'inscrire" else None
        # Opérations
        self.connexion() # Gérer la connexion
        self.inscription() # Gérer l'inscription

    def get_info(self):
        # Éléments communs / Réccupération données saisit
        self.pseudo = self.entry_pseudo.get()
        self.mdp = self.entry_mdp.get()
        self.confirm_mdp = self.entry_confirm_mdp.get() if self.bouton_valider.cget("text") == "S'inscrire" else None

    def set_nom_joueur(self, pseudo):
        self.pseudo = pseudo
        self.accueil.set_nom_joueur(self.pseudo)
    
    def get_nom_joueur(self):
        return self.pseudo

    def connexion(self):
        if self.bouton_valider.cget("text") == "Se connecter":
            if os.path.exists("utilisateurs.json"):
                with open("utilisateurs.json", "r") as f:
                    utilisateurs = json.load(f)

                self.get_info()
                # Conditions de connexion    
                if self.pseudo in utilisateurs:
                    # Récupérer le mot de passe haché
                    hashed_mdp = utilisateurs[self.pseudo]["password"].encode('utf-8')
                    if bcrypt.checkpw(self.mdp.encode('utf-8'), hashed_mdp):
                        self.set_nom_joueur(self.pseudo)
                        self.afficher_connexion_reussi()
                    else:
                        self.entry_mdp.delete(0, "end")
                        self.entry_mdp.configure(placeholder_text="* Mot de passe erroné", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                        return
                # Connexion non abouti 
                if not self.pseudo:
                    self.entry_pseudo.configure(placeholder_text="* Veuillez saisir un nom", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                    return 
                
                elif self.pseudo and not self.mdp:
                    self.entry_mdp.configure(placeholder_text="* Veuillez saisir un mot de passe", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                    return  
                
                elif not self.pseudo in utilisateurs and len(self.pseudo) > 0:
                    self.entry_pseudo.delete(0, "end")
                    self.entry_pseudo.configure(placeholder_text="* Utilisateur introuvable", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                    return
            else:
                print("Aucun utilisateur enregistré. Veuillez vous inscrire d'abord.")

    def inscription(self):
        self.confirm_mdp = self.entry_confirm_mdp.get()
        if self.bouton_valider.cget("text") == "S'inscrire":
            if os.path.exists("utilisateurs.json"):
                with open("utilisateurs.json", "r") as f:
                    utilisateurs = json.load(f)
            else:
                utilisateurs = {}

            self.get_info()
            # Conditions d'inscription 
            if self.pseudo in utilisateurs:
                self.entry_pseudo.delete(0, "end")
                self.entry_pseudo.configure(placeholder_text="* Nom déja utilisé", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                return
            
            elif not self.pseudo:
                self.entry_pseudo.configure(placeholder_text="* Veuillez saisir un nom", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                return
            
            elif len(self.pseudo) < 4:
                self.set_nom_joueur("")
                self.entry_pseudo.delete(0, "end")
                self.entry_pseudo.configure(placeholder_text="* Nom trop court", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                return
            
            elif not self.mdp and not self.confirm_mdp:
                self.entry_mdp.configure(placeholder_text="* Veuillez saisir un mot de passe", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                self.entry_confirm_mdp.configure(placeholder_text="* Veuillez saisir un mot de passe", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                return
            
            elif len(self.mdp) < 5:
                self.entry_mdp.delete(0, "end")
                self.entry_mdp.configure(placeholder_text="* Mot de passe trop court", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                return 
            
            elif self.mdp == self.pseudo:
                self.entry_mdp.delete(0, "end")
                self.entry_mdp.configure(placeholder_text="* Doit être différent du nom", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                return
            
            caract_special = ['!', '@', '#', '$', '%', '?', '&', '*', '_', '-', '=', '+', ';', '<', '>']
            for c in caract_special:
                if not any(c in self.mdp for c in caract_special):
                    self.entry_mdp.delete(0, "end")
                    self.entry_mdp.configure(placeholder_text="* Doit contenir un caractère spécial", placeholder_text_color="#F14156", font=("Arial", 24, "bold"))
                    return 
            
            if self.mdp != self.confirm_mdp:
                self.entry_mdp.delete(0, "end")
                self.entry_mdp.configure(placeholder_text="* Les mots de passes doivent correspondre", placeholder_text_color="#F14156", font=("Arial", 19, "bold"))
                self.entry_confirm_mdp.delete(0, "end")
                self.entry_confirm_mdp.configure(placeholder_text="* Les mots de passes doivent correspondre", placeholder_text_color="#F14156", font=("Arial", 19, "bold"))
                return
            
            elif self.mdp == self.confirm_mdp:
                # Hacher le mot de passe
                hashed_mdp = bcrypt.hashpw(self.mdp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                utilisateurs[self.pseudo] = {"password": hashed_mdp}
                with open("utilisateurs.json", "w") as f:
                    json.dump(utilisateurs, f, indent=4)
                self.bouton_valider.configure(text="Réussi!")
                self.afficher_inscription_reussi()

    def afficher_connexion_reussi(self):
        self.masquer_formulaire()
        self.label_connexion_reussi = ctk.CTkLabel(self.main_frame, text="Connexion réussi!", font=("Arial", 100, "bold"), text_color="#16a085")
        self.label_connexion_reussi.grid(row=0, column=0, columnspan=2, pady=(0, 100))
        self.master.after(1000, lambda: [self.label_connexion_reussi.grid_remove(), self.accueil.afficher_accueil()])

    def afficher_inscription_reussi(self):
        self.masquer_formulaire()
        self.label_inscription_reussi = ctk.CTkLabel(self.main_frame, text="Inscription réussi!", font=("Arial", 100, "bold"), text_color="#16a085")
        self.label_inscription_reussi.grid(row=0, column=0, columnspan=2, pady=(0, 100))
        self.master.after(1000, lambda: [self.label_inscription_reussi.grid_remove(), self.afficher_connexion()])

    def masquer_formulaire(self):   
        self.bouton_connexion.grid_remove()
        self.bouton_inscription.grid_remove()
        self.entry_pseudo.grid_remove()
        self.entry_mdp.grid_remove()
        self.entry_confirm_mdp.grid_remove()
        self.bouton_valider.grid_remove()
        self.bouton_retour.grid_remove()