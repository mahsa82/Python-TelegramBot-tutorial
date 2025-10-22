import telebot
import os
import json

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

#Handle '/start' and '/help'
@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    # bot.reply_to(message,"""\
    #     Hi there, I am mahsaBot.
    #     """)
    bot.send_message(message.chat.id,json.dumps(message.chat.__dict__,indent=4,ensure_ascii=False))

bot.infinity_polling()