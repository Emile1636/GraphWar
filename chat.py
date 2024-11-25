import customtkinter as ctk
from PIL import Image, ImageTk
from transformers import pipeline 

class Chat(ctk.CTkFrame):
    def __init__(self, master, main_frame, accueil):
        super().__init__(master)  
        self.main_frame = main_frame
        self.accueil = accueil
        self.ask_no = 0
        self.size_text = 10.8
        self.questions = []
        self.reponses = []
        self.creation_chat()
        self.creation_chatbot()
    
    def creation_chat(self): # afficher une image vide pour le uyser des le début
        # Images
        # Chargement et conversion de l'image en CTkImage
        image_empty = Image.open("./images/empty.png")
        ctk_image_empty = ctk.CTkImage(image_empty, size=(50, 50)) 
        self.empty_pp = ctk.CTkLabel(self.main_frame, image=ctk_image_empty, text="")

        image_bot = Image.open("./images/bot_pp.png")
        ctk_image_bot = ctk.CTkImage(image_bot, size=(50, 50)) 
        self.bot_pp1 = ctk.CTkLabel(self.main_frame, image=ctk_image_bot, text="")
        self.bot_pp2 = ctk.CTkLabel(self.main_frame, image=ctk_image_bot, text="")
        self.bot_pp3 = ctk.CTkLabel(self.main_frame, image=ctk_image_bot, text="")
        self.bot_pp4 = ctk.CTkLabel(self.main_frame, image=ctk_image_bot, text="")

        image_user = Image.open("./images/user_pp2.png")
        ctk_image_user = ctk.CTkImage(image_user, size=(50, 50))
        self.user_pp1 = ctk.CTkLabel(self.main_frame, image=ctk_image_user, text="")
        self.user_pp2 = ctk.CTkLabel(self.main_frame, image=ctk_image_user, text="")
        self.user_pp3 = ctk.CTkLabel(self.main_frame, image=ctk_image_user, text="")

        # Zones de textes afficher messages #121D22
        self.tampon = ctk.CTkLabel(self.main_frame, text="", width=1000, height=1, fg_color="#121D22")
        self.text_B1 = ctk.CTkLabel(self.main_frame, text="", width=475, height=65,corner_radius=35, fg_color="white", text_color="black", font=("Arial", 20, "bold"), anchor="w") # fg_color="#16a085", text_color="#F8F6F6"
        self.text_U1 = ctk.CTkLabel(self.main_frame, text="", width=700, height=65,corner_radius=35, fg_color="#121D22", text_color="black", font=("Arial", 20, "bold"), anchor="e")
        self.text_B2 = ctk.CTkLabel(self.main_frame, text="", width=700, height=65,corner_radius=35, fg_color="#121D22", text_color="black", font=("Arial", 20, "bold"), anchor="w")
        self.text_U2 = ctk.CTkLabel(self.main_frame, text="", width=700, height=65,corner_radius=35, fg_color="#121D22", text_color="black", font=("Arial", 20, "bold"), anchor="e")
        self.text_B3 = ctk.CTkLabel(self.main_frame, text="", width=700, height=65,corner_radius=35, fg_color="#121D22", text_color="black", font=("Arial", 20, "bold"), anchor="w")
        self.text_U3 = ctk.CTkLabel(self.main_frame, text="", width=700, height=65,corner_radius=35, fg_color="#121D22", text_color="black", font=("Arial", 20, "bold"), anchor="e")
        self.text_B4 = ctk.CTkLabel(self.main_frame, text="", width=700, height=65,corner_radius=35, fg_color="#121D22", text_color="black", font=("Arial", 20, "bold"), anchor="w")
       
        # Zone d'écriture
        self.entry_question = ctk.CTkEntry(self.main_frame, placeholder_text="Ask your question...", placeholder_text_color="#B0B0B0", width=800, height=60,corner_radius=25, fg_color="white", text_color="black", font=("Arial", 20, "bold"))
        self.entry_question.bind("<Return>", self.question_enter) # Si la touche enter 

        # Boutons de retour
        self.bouton_retour = ctk.CTkButton(self.main_frame, text="Back", command=lambda:[self.masquer_chat()], corner_radius=30, width=150, height=40, fg_color="#e74c3c", hover_color="#d93c3a", font=("Arial", 24, "bold"))

    def creation_chatbot(self):
        # Charger le modèle de question-réponse
        model_name = "bert-large-uncased-whole-word-masking-finetuned-squad" # Autre : "deepset/roberta-base-squad2"
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name, device=0)  # Utiliser le GPU 
        with open('context.txt', 'r') as file:
            self.context = file.read()

    def generer_reponse(self, question):
        result = self.nlp(question=question, context=self.context) 
        reponse = result.get('answer', '').strip() 

        if not reponse or len(reponse.split()) < 2:
            reponse = "Désolé, je n'ai pas pu répondre clairement. Réessayez avec une reformulation."
        else:
            reponse = reponse.capitalize()
        return reponse

    def afficher_chat(self):
        # Positionner les avatars et messages
        self.empty_pp.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.bot_pp1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.text_B1.configure(text="Hello, I'm excited to answer your questions", fg_color="white")
        self.text_B1.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        self.text_U1.grid(row=1, column=1, padx=20, pady=10, sticky="e")
        self.text_B2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        
        self.text_U2.grid(row=3, column=1, padx=20, pady=10, sticky="e")
        self.text_B3.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        self.text_U3.grid(row=5, column=1, padx=20, pady=10, sticky="e")
        self.text_B4.grid(row=6, column=1, padx=20, pady=10, sticky="w")
        
        # Zone d'entrée
        self.entry_question.grid(row=8, column=0, columnspan=3, padx=20, pady=10)

        # Bouton retour
        self.bouton_retour.grid(row=9, column=1, padx=10, pady=(30,10))
        
        # Ajuster les colonnes
        self.main_frame.columnconfigure(0, weight=1)  # Avatar à gauche
        self.main_frame.columnconfigure(1, weight=4)  # Messages au centre
        self.main_frame.columnconfigure(2, weight=1)  # Avatar à droite
        self.tampon.grid(row=7, column=1, padx=None, pady=(0,50))

    def question_enter(self, event):
        if self.ask_no == 0: 
            self.ask_no += 1
            self.Q_A_1()
            self.empty_pp.grid_remove()
        elif self.ask_no == 1: 
            self.ask_no += 1
            self.Q_A_2()
        elif self.ask_no == 2:
            self.ask_no += 1
            self.Q_A_3()
        elif self.ask_no >= 3:
            self.ask_no += 1
            self.Q_A_4_et_plus()

    def get_question(self):
        question = self.entry_question.get()
        self.questions.append(question)
        self.entry_question.delete(0, "end")
        self.main_frame.focus_set()
        self.entry_question.configure(placeholder_text="Ask other question...")

    def Q_A_1(self):
        # Récupérer la question et rénitialiser
        self.get_question()
        question = self.questions[0]

        # Afficher la question
        self.user_pp1.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.text_U1.configure(text=question, fg_color="#AEC0D5", width=(self.size_text * len(question)))

        #Générer la réponse
        reponse = self.generer_reponse(question)
        self.reponses.append(reponse)

        # Afficher la réponse
        self.bot_pp2.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.text_B2.configure(text=reponse, fg_color="white", width=(self.size_text * len(reponse)))

    def Q_A_2(self):
        # Récupérer la question et rénitialiser
        self.get_question()
        question = self.questions[1]

        # Afficher la question
        self.user_pp2.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.text_U2.configure(text=question, fg_color="#AEC0D5", width=(self.size_text * len(question)))

        #Générer la réponse
        reponse = self.generer_reponse(question)
        self.reponses.append(reponse)
        
        # Afficher la réponse
        self.bot_pp3.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.text_B3.configure(text=reponse, fg_color="white", width=(self.size_text * len(reponse)))

    def Q_A_3(self):
        # Récupérer la question et rénitialiser
        self.get_question()
        question = self.questions[2]

        # Afficher la question
        self.user_pp3.grid(row=5, column=2, padx=10, pady=10, sticky="e")
        self.text_U3.configure(text=question, fg_color="#AEC0D5", width=(self.size_text * len(question)))

        #Générer la réponse
        reponse = self.generer_reponse(question)
        self.reponses.append(reponse)
        
        # Afficher la réponse
        self.bot_pp4.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.text_B4.configure(text=reponse, fg_color="white", width=(self.size_text * len(reponse)))

    def Q_A_4_et_plus(self):
        # Récupérer la question et rénitialiser
        self.get_question()
        question = self.questions[self.ask_no - 1]

        # Afficher la question
        self.user_pp3.grid(row=5, column=2, padx=10, pady=10, sticky="e")
        self.text_U3.configure(text=question, fg_color="#AEC0D5", width=(self.size_text * len(question)))

        #Générer la réponse
        reponse = self.generer_reponse(question)
        self.reponses.append(reponse)

        # Afficher la réponse
        self.bot_pp4.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.text_B4.configure(text=reponse, fg_color="white", width=(self.size_text * len(reponse)))

        # Décaler la conversation
        self.text_B1.configure(text=self.reponses[self.ask_no - 4], width=(self.size_text * len(self.reponses[self.ask_no - 4])))
        self.text_B2.configure(text=self.reponses[self.ask_no - 3], width=(self.size_text * len(self.reponses[self.ask_no - 3])))
        self.text_B3.configure(text=self.reponses[self.ask_no - 2], width=(self.size_text * len(self.reponses[self.ask_no - 2])))

        self.text_U1.configure(text=self.questions[self.ask_no - 3], width=(self.size_text * len(self.questions[self.ask_no - 3])))
        self.text_U2.configure(text=self.questions[self.ask_no - 2], width=(self.size_text * len(self.questions[self.ask_no - 2])))

    def masquer_chat(self):
        # Photos et Messages
        self.bot_pp1.grid_remove()
        self.text_B1.configure(text="", fg_color="#121D22")
        self.text_B1.grid_remove()
        self.user_pp1.grid_remove()
        self.text_U1.configure(text="", fg_color="#121D22")
        self.text_U1.grid_remove()
        self.bot_pp2.grid_remove()
        self.text_B2.configure(text="", fg_color="#121D22")
        self.text_B2.grid_remove()
        self.user_pp2.grid_remove()
        self.text_U2.configure(text="", fg_color="#121D22")
        self.text_U2.grid_remove()
        self.bot_pp3.grid_remove()
        self.text_B3.configure(text="", fg_color="#121D22")
        self.text_B3.grid_remove()
        self.user_pp3.grid_remove()
        self.text_U3.configure(text="", fg_color="#121D22")
        self.text_U3.grid_remove()
        self.bot_pp4.grid_remove()
        self.text_B4.configure(text="", fg_color="#121D22")
        self.text_B4.grid_remove()

        # Autres éléments
        self.empty_pp.grid_remove()
        self.tampon.grid_remove()
        self.bouton_retour.grid_remove()
        self.entry_question.delete(0, "end")
        self.entry_question.grid_remove()

        # Reset
        for col in range(self.main_frame.grid_size()[1]): 
            self.main_frame.columnconfigure(col, weight=0) 
            self.main_frame.columnconfigure(col, minsize=0) 
            self.main_frame.columnconfigure(col, pad=0)
        self.ask_no = 0
        self.questions.clear()
        self.reponses.clear()
        self.accueil.jeu.lancer_jeu()
