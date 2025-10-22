import telebot
import os
import json
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    # bot.reply_to(message,"""\
    #     Hi there, I am mahsaBot.
    #     """)
    bot.send_message(message.chat.id,json.dumps(message.chat.__dict__,indent=4,ensure_ascii=False))

# Handels all sent documents and audio files
@bot.message_handler(content_types =['document','audio'])
def handle_docs_audio(message):
    if message.content_type == "document":
        print("Its a document.")
    elif message.content_type == 'audio':
        print("Its an audio")


# Handles all messages for which the lambda returns True


@bot.message_handler(func=lambda message: message.text == "hello")
def handle_text_doc(message):
    bot.send_message(message.chat.id, "Hi dear, I hope you the best day!")
    
@bot.message_handler(func=lambda message:True)
def handle_all_text(message):
    bot.send_message(message.chat.id, "Thank you for your suggestion.")
    
# start polling        
bot.infinity_polling()
    