import telebot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import constants
constants.DEFAULT_LANGUAGE_TO_SPACY_MODEL_MAP['fr'] = 'fr_core_news_sm'

# Remplacez par le token de votre bot Telegram

TOKEN = '8301017725:AAE5GTEmMP8tJvy3OxJcLEtsTqpC644oCoo'


# Suggestions de questions a proposer apres chaque réponse
SUGGESTIONS = [
    "Quelles sont les filières à l'UCBC ?",
    "Comment s'inscrire à l'UCBC ?",
    "Où se trouve l'UCBC ?",
    "Quels sont les frais académiques ?",
    "Comment contacter l'UCBC ?",
    "pourquoi l'ucbc"
]


# Creation et entrainement du chatbot local (ChatterBot)
local_bot = ChatBot(
    'UCBCBot',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation'
    ],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///ucbc_bot_database.sqlite3',
    read_only=True
)
# Entrainer le bot avec des questions-reponses sur l'UCBC
trainer = ListTrainer(local_bot)
trainer.train([
    "Bonjour", "Bonjour, comment puis-je vous aider concernant l'UCBC ?",
    "Quelles sont les filières à l'UCBC ?", "Les principales filières sont :Faculte de  Technologie et science de l'ingenieur, Faculte de Gestion et d'Economie, Faculte de Theologie, Faculte d'Agronomie, etc.",
    "Comment s'inscrire a l'UCBC ?", "Les inscriptions se font chaque année de juillet à septembre. Plus d'infos sur le site officiel.",
    "Où se trouve l'UCBC ?", "L'UCBC est située à Beni, Nord-Kivu, RDC.",
    "Quel est le site web de l'UCBC ?", "Le site officiel de l'UCBC est https://ucbc.org/",
    "Quels sont les frais académiques ?", "Les frais académiques varient selon la filière. Contactez le service académique pour plus de détails.",
    "Comment contacter l'UCBC ?", "Vous pouvez contacter l'UCBC au +243 999 999 999 ",
    "Pourquoi UCBC?", "Le programme d'études de l'UCBC intègre la rigueur académique, la formation de personnages, la recherche communautaire et l'apprentissage par le service dans un nouveau programme unique de licence de 4 ans dans le cadre du nouveau modèle éducatif, L.M.D, du Congo. UCBC sera l'une des trois universités congolaises accréditées à initier le processus de Bologne L.M.D., modèle d'éducation au Congo à partir d'octobre 2010. Pour le moment, nous restructurons notre modèle académique actuel qui a été enseigné pendant trois ans pour répondre à la vision du gouvernement pour l'enseignement supérieur et fournir une éducation unique qui forme les étudiants à diriger la transformation du Congo.",
    ""




])
# Fonction pour obtenir une reponse de l'IA
def get_ai_answer(question):
    # Utiliser uniquement ChatterBot local pour repondre
    try:
        local_response = local_bot.get_response(question)
        return str(local_response)
    except Exception as e:
        return f"Erreur IA locale: {e}"


bot = telebot.TeleBot(TOKEN)

# Definir le menu de commandes Telegram pour le bot (affiche a cote de la zone de saisie)
bot.set_my_commands([

    telebot.types.BotCommand('start', 'Démarrer le bot'),
    telebot.types.BotCommand('info','information sur le bot'),
    telebot.types.BotCommand('help', 'Aide sur le bot'),
    telebot.types.BotCommand('filieres', 'Voir les filières'),
    telebot.types.BotCommand('contact', 'Contact de l\'UCBC'),
    telebot.types.BotCommand('inscription', 'Infos sur l\'inscription'),
    telebot.types.BotCommand('siteweb', 'Site officiel de l\'UCBC')
])
# commande /start
@bot.message_handler(commands=['start',])
def send_welcome(message):
    bot.reply_to(message, "Bonjour je suis un chatbot creer par DANIEL pour vous aidez a vous fammiliariser avec L'UCBC! Posez-moi une question sur l'UCBC (adresse, contact, filières, inscription, etc.).")

# Commande /filières
@bot.message_handler(commands=['filières', 'filieres'])
def send_filieres(message):
    bot.reply_to(message, "Les principales filières sont : .")

# Commande /contact
@bot.message_handler(commands=['contact'])
def send_contact(message):
    bot.reply_to(message, "Vous pouvez contacter l'UCBC au +243 000 000 000 ... ou par email à ...")

# Commande /inscription
@bot.message_handler(commands=['inscription'])
def send_inscription(message):
    bot.reply_to(message, "Les inscriptions se font chaque année de juillet à septembre. Plus d'infos sur le site officiel.")

# Commande /siteweb
@bot.message_handler(commands=['siteweb'])
def send_siteweb(message):
    bot.reply_to(message, "Le site officiel de l'UCBC est https://ucbc.org/")

    
# Commande /info
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "Le bot UCBC est conçu pour répondre à vos questions sur l'Université Chrétienne Bilingue du Congo (UCBC). Vous pouvez poser toutes vos questions concernant l'université et obtenir des réponses précises.")

# Commande /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Commandes disponibles : /start, /help, /info, /filieres, /contact, /inscription, /siteweb, /info")


# Handler principal : repond a toute question reçue
@bot.message_handler(func=lambda message: True)
def answer_question(message):
    question = message.text.lower()


    # Si la question contient 'logo', on envoie l'image du logo UCBC
    if 'logo' in question:
        try:
            with open('ucbc_logo.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Voici le logo de l'UCBC.")
        except Exception:
            bot.reply_to(message, "Logo non disponible.")
        return

    # Si la question contient 'plan' ou 'carte', on envoie l'image du plan/carte
    if 'plan' in question or 'carte' in question:
        try:
            with open('ucbc_plan.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Voici le plan de l'UCBC.")
        except Exception:
            bot.reply_to(message, "Plan non disponible.")
        return
  

    # Sinon, on utilise l'IA (OpenAI ou ChatterBot local) pour repondre
    ai_response = get_ai_answer(message.text)
    bot.reply_to(message, ai_response)

    # Apres la reponse principale, proposer des suggestions
    suggestions_text = "Vous pouvez aussi demander par exemple :\n" + "\n".join(f"- {q}" for q in SUGGESTIONS)
    bot.reply_to(message, suggestions_text)

if __name__ == "__main__":
    print("Bot UCBC en cours d'exécution...")
    bot.polling()
