import telebot
# from telebot import types
import markup
import db_cmd
import ast
from settings import token

bot = telebot.TeleBot(token)

@bot.message_handler(content_types="photo")
def photo(m):
    cid = m.chat.id
    print(m)


bot.polling()