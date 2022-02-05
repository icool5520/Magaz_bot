import telebot
# from telebot import types
import markup
import db_cmd
import ast
from settings import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        db_cmd.check_user_id(uid)
        bot.send_message(cid, "Магазин", reply_markup=markup.gen_markup())
    except Exception as ex:
        print('start_msg:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "start")
def callback_main_menu(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        db_cmd.check_user_id(uid)
        bot.send_message(cid, "Магазин", reply_markup=markup.gen_markup())
    except Exception as ex:
        print('callback_main_menu:', ex)

@bot.message_handler(commands=['admin'])
def command_admin(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if cid==uid and db_cmd.check_user_is_admin(uid):
            bot.send_message(cid, "Меню администратора", reply_markup=markup.gen_admin_markup())
    except Exception as ex:
        print('start_msg:', ex)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def callback_categors(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            categor = str(call.data[4:])
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Продукция категории: " + str(categor),
                                  reply_markup=markup.products_menu(categor))
    except Exception as ex:
        print('callback_categors:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("prod_"))
def callback_products(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            id_product = int(call.data[5:])
            info = db_cmd.get_info_product(id_product)
            data = db_cmd.get_data(uid)
            new_data = dict(ast.literal_eval(data))
            new_data['id'] = id_product
            db_cmd.up_data(uid, str(new_data))
            bot.send_photo(cid, photo=info[5])
            cart_content = db_cmd.get_cart(uid)
            if cart_content is None or id_product not in list(ast.literal_eval(cart_content[1])):
                bot.send_message(cid, f"Название: {info[1]}\nЦена: {info[3]}\nИнфо: {info[4]}",
                             reply_markup=markup.buy(id_product))
            else:
                lst_id_product = list(ast.literal_eval(cart_content[1]))
                num = lst_id_product.count(id_product)
                bot.send_message(cid, f"Название: {info[1]}\nЦена: {info[3]}\nИнфо: {info[4]}" +
                                 f"\n\n\U00002705Добавлено в корзину {num} - шт.", reply_markup=markup.buy(id_product))
    except Exception as ex:
        print('callback_products:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def callback_add_to_cart(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            id_product = int(call.data[4:])
            info = db_cmd.get_info_product(id_product)
            price_product = info[3]  # integer
            cart_content = db_cmd.get_cart(uid)
            if cart_content is None:
                print('Пустая корзина')
                lst_id_product = []
                lst_id_product.append(id_product)
                db_cmd.set_cart(uid, str(lst_id_product), price_product)
            else:
                lst_id_product = ast.literal_eval(cart_content[1])
                lst_id_product.append(id_product)
                amount = price_product + cart_content[2]
                db_cmd.up_cart(uid, str(lst_id_product), amount)
            num = lst_id_product.count(id_product)
            bot.edit_message_text(chat_id=cid, message_id=mid, text=f"Название: {info[1]}\nЦена: {info[3]}\nИнфо: {info[4]}" +
                                 f"\n\n\U00002705Добавлено в корзину - {num} шт.", reply_markup=markup.buy(id_product))
    except Exception as ex:
        print('callback_add_to_cart:', ex)


if __name__ == '__main__':
    bot.polling()
