from telebot import types
import db_cmd


def gen_markup():
    markup = types.InlineKeyboardMarkup()
    categors = db_cmd.get_categors()
    categors_kb = []
    for i in categors:
        categors_kb.append(types.InlineKeyboardButton(i, callback_data=f"cat_{i}"))
    btn1 = types.InlineKeyboardButton("Корзина  \U0001F6CD", callback_data="cart")
    markup.add(*categors_kb)
    markup.row(btn1)
    return markup


def gen_admin_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Заказы", callback_data="orders")
    btn2 = types.InlineKeyboardButton("Товары", callback_data="tovs")
    markup.add(btn1)
    markup.add(btn2)
    return markup


def gen_empty_cart_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Главное меню", callback_data="start")
    markup.add(btn1)
    return markup


def gen_cart_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("\U00002705Оформить заказ", callback_data="confirm_order")
    btn2 = types.InlineKeyboardButton("\U0000274CУдалить заказ", callback_data="delete_order")
    btn3 = types.InlineKeyboardButton("Главное меню", callback_data="start")
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


def gen_products_menu_markup(_categor):
    markup = types.InlineKeyboardMarkup()
    products = db_cmd.get_products(_categor)
    for i in products:
        markup.add(types.InlineKeyboardButton(i[1], callback_data=f"prod_{i[0]}"))
    btn1 = types.InlineKeyboardButton("<< Назад", callback_data="start")
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

def buy(_id_product):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Добавить в корзину", callback_data=f"add_{_id_product}")
    btn2 = types.InlineKeyboardButton("Перейти в корзину  \U0001F6CD", callback_data="cart")
    btn3 = types.InlineKeyboardButton("Главное меню", callback_data="start")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    return markup
