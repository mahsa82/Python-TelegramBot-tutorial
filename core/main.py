import telebot
from telebot import apihelper
import os
import json
import logging
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton , InlineKeyboardButton,InlineKeyboardMarkup
import requests


apihelper.ENABLE_MIDDLEWARE = True
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help','start'])
# def send_welcome(message):
#     # bot.reply_to(message,"""\
#     #     Hi there, I am mahsaBot.
#     #     """)
#     bot.send_message(message.chat.id,json.dumps(message.chat.__dict__,indent=4,ensure_ascii=False))

# # Handels all sent documents and audio files
# @bot.message_handler(content_types =['document','audio'])
# def handle_docs_audio(message):
#     if message.content_type == "document":
#         print("Its a document.")
#     elif message.content_type == 'audio':
#         print("Its an audio")


# # Handles all messages for which the lambda returns True


# @bot.message_handler(func=lambda message: message.text == "hello")
# def handle_text_doc(message):
#     bot.send_message(message.chat.id, "Hi dear, I hope you the best day!")
    
# # @bot.message_handler(func=lambda message:True)
# # def handle_all_text(message):
# #     bot.send_message(message.chat.id, "Thank you for your suggestion.")
    
# @bot.middleware_handler(update_types=['message'])
# def modify_message(bot_instance,message):
#     message.another_text = message.text + ':changed'
    
# @bot.message_handler(func=lambda message:True)
# def reply_modified(message):
#     logger.info("triggered welcome")
#     bot.reply_to(message,"""Hi this is a sample for learning telegram bot in python.""")

# @bot.message_handler(commands=["setname"])
# def setup_name(message):
#     bot.send_message(message.chat.id,"what is your name?")
#     bot.register_next_step_handler(message,callback=assign_name)
    
# def assign_name(message,*args,**kwargs):
#     # logger.info(args)
#     # logger.info(kwargs)
#     name = message.text
#     bot.send_message(message.chat.id,f"welcome {name} to my bot")

# # start polling        
# bot.infinity_polling()

# @bot.message_handler(func=lambda message:True)
# def handle_all_text(message):
#     bot.send_message(message.chat.id, "Thank you for your suggestion.")
# #handeling edited message
# @bot.edited_message_handler(func=lambda message:True)
# def send_welcome(message):
#     print("triggered for edited message.")
    
# #display this markup
#     bot.send_message(chat_id,'Text')
#     bot.send_message(message.chat.id,"""Hi this is a sample for learning telegram bot in python""",reply_markup=markup)
'''
# a small exercise
@bot.message_handler(commands=['start'])
def show_home(message):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Choose your option:'
    )
    markup.add(KeyboardButton('help'), KeyboardButton('about'))
    markup.add(KeyboardButton('This is just for so'))

    bot.send_message(message.chat.id, "Hi I'm mahsa🖐Please choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'help')
def send_help(msg):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Admin 👩🏻‍💻", url="https://t.me/example"))
    bot.send_message(
        msg.chat.id,
        "How can I help you? You can contact the admin below 👇",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == 'about')
def send_about(msg):
    bot.send_message(msg.chat.id, "This bot is for test. Enjoy it 😎")


@bot.message_handler(func=lambda message: message.text == "This is just for so")
def ask_so(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Yes", callback_data="Yes_so"),
        InlineKeyboardButton("No", callback_data="No_so")
    )
    bot.send_message(message.chat.id, "Are you so?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def reply_call(call):
    chat_id = call.message.chat.id
    message_id = call.message.id

    if call.data == "Yes_so":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Yes", callback_data="Confirm_so"),
            InlineKeyboardButton("No", callback_data="No_so")
        )
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text='Are you sure?',
            reply_markup=markup
        )

    elif call.data == "Confirm_so":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text='Hi so 😉🖐 You can pass all your challenges successfully 😎'
        )

    elif call.data == "No_so":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text='Oops 😅 You are not so!'
        )
        show_home(call.message)  # return back to home page
'''


# file_download
if not os.path.exists("downloads"):
    os.makedirs("downloads")

DOWNLOAD_DIR = "downloads/"

@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.send_message(msg.chat.id,"Give me a valid url for a file and i will download and upload it for you😉")

def download_file(url):
    local_filename = url.split('/')[-1]
    file_path = DOWNLOAD_DIR + local_filename
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path
            
@bot.message_handler(func=lambda message: True)
def download_file_url(message):
    logger.info(message.text)
    url = message.text
    try:
        file_path = download_file(url)
        bot.send_document(chat_id=message.chat.id, reply_to_message_id=message.id, document=open(
            file_path, "rb"), caption="file downloaded successfully, ENJOY!")
        os.remove(file_path)
    except:
        bot.reply_to(message, text="problem downloading the requested file")


# start polling        
bot.infinity_polling()


    