from telebot import types
import db_cmd


def gen_markup():
    markup = types.InlineKeyboardMarkup()
    categors = db_cmd.get_categors()
    categors_kb = []
    for i in categors:
        categors_kb.append(types.InlineKeyboardButton(i, callback_data=f"cat_{i}"))
    btn1 = types.InlineKeyboardButton("Корзина", callback_data="cart")
    markup.add(*categors_kb)
    markup.row(btn1)
    return markup

def products_menu(_categor):
    markup = types.InlineKeyboardMarkup()
    products = db_cmd.get_products(_categor)
    for i in products:
        markup.add(types.InlineKeyboardButton(i[1], callback_data=f"prod_{i[0]}"))
    btn1 = types.InlineKeyboardButton("Главное меню", callback_data="start")
    markup.row(btn1)
    return markup

# версия с выводом маленьких кнопок

# def products_menu(_categor):
#     markup = types.InlineKeyboardMarkup()
#     products = db_cmd.get_products(_categor)
#     products_kb = []
#     for i in products:
#         products_kb.append(types.InlineKeyboardButton(i[1], callback_data=f"prod_{i[0]}"))
#     btn1 = types.InlineKeyboardButton("Главное меню", callback_data="start")
#     markup.add(*products_kb)
#     markup.row(btn1)
#     return markup

def buy():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Добавить в корзину", callback_data="add")
    btn2 = types.InlineKeyboardButton("Главное меню", callback_data="start")
    markup.add(btn1)
    markup.add(btn2)
    return markup
