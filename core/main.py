import telebot
from telebot import apihelper
import os
import json
import logging
from dotenv import load_dotenv

apihelper.ENABLE_MIDDLEWARE = True
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

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
    
# @bot.message_handler(func=lambda message:True)
# def handle_all_text(message):
#     bot.send_message(message.chat.id, "Thank you for your suggestion.")
    
@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance,message):
    message.another_text = message.text + ':changed'
    
@bot.message_handler(func=lambda message:True)
def reply_modified(message):
    logger.info("triggered welcome")
    bot.reply_to(message,"""Hi this is a sample for learning telegram bot in python.""")

@bot.message_handler(commands=["setname"])
def setup_name(message):
    bot.send_message(message.chat.id,"what is your name?")
    bot.register_next_step_handler(message,callback=assign_name)
    
def assign_name(message,*args,**kwargs):
    # logger.info(args)
    # logger.info(kwargs)
    name = message.text
    bot.send_message(message.chat.id,f"welcome {name} to my bot")

# start polling        
bot.infinity_polling()
    