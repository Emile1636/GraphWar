from transformers import pipeline

# Créer le pipeline en spécifiant le modèle et le tokenizer
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", device=0)

# Contexte structuré
with open('context.txt', 'r') as file:
    context = file.read()

# Questions
questions = [
    "What is the form of a linear function?",
    "What is the form of a quadratic function?",
    "What is the form of a sinus function?",
    "What is the form of a cosine function?",
    "What is the form of an exponential function?",

    "How to increase a linear function?",
    "How to increase a quadratic function?",
    "How to increase a sinus function?",
    "How to increase a cosine function?",
    "How to increase an exponential function?",

    "How to make a linear function goes down?",
    "How to make a quadratic function goes down?",
    "How to make a sinus function goes down?",
    "How to make a cosine function goes down?",
    "How to make an exponential function goes down?"
]


# Boucle pour obtenir les réponses
for question in questions:
    result = qa_pipeline(question=question, context=context)
    reponse = result.get('answer', '').strip() 

    if not reponse or len(reponse.split()) < 2:
        reponse = "Désolé, je n'ai pas pu répondre clairement. Réessayez avec une reformulation."
    else:
        reponse = reponse.capitalize()

    print(f"Question: {question}\nAnswer: {result['answer']}\n")
