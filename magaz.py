import telebot
# from telebot import types
import markup
import db_cmd
import ast
from settings import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def message_handler(message):
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
            bot.send_message(cid, f"Название: {info[1]}\nЦена: {info[3]}\nИнфо: {info[4]}",
                             reply_markup=markup.buy())
    except Exception as ex:
        print('callback_products:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "add")
def callback_add_to_cart(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            data = []
            data = dict(ast.literal_eval(db_cmd.get_data(uid)))
            id_product = data['id']  # integer
            price_product = db_cmd.get_info_product(id_product)[3]  # integer
            cart_content = db_cmd.get_cart(uid)
            print(cart_content)
            if cart_content is None:
                lst_id_product = []
                lst_id_product.append(id_product)
                db_cmd.set_cart(uid, str(lst_id_product), price_product)
            else:
                lst_id_product = ast.literal_eval(cart_content[1])
                lst_id_product.append(id_product)
                amount = price_product + cart_content[2]
                db_cmd.up_cart(uid, str(lst_id_product), amount)
    except Exception as ex:
        print('callback_add_to_cart:', ex)


'''
@bot.message_handler(commands=['admin'])
def admin_start(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		if cid == uid and db_cmd.check_admin(uid):
			db_cmd.upd_state_admin(uid, "menu_admin")
			bot.send_message(chat_id=cid, text="Меню администратора", reply_markup=markup.gen_markup_admin())
	except Exception as ex:
		print('admin_start:', ex)


@bot.message_handler(commands=['edit_myprofile'])
def edit_myprofile(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		if cid == uid:
			db_cmd.upd_state_user(uid, "view_myprofile")
			myprofile_data = db_cmd.get_user_myprofile(uid)
			if myprofile_data[4] != '-':
				photo_id = f"{myprofile_data[4]}"
			else:
				photo_id = "AgACAgIAAxkBAAIEpWHxHvFZMAlLAmuluP1Nz-z_lugQAAIHuDEbBi6JSz10nVNPG1V-AQADAgADeAADIwQ"
			bot.send_photo(chat_id=cid, photo=photo_id, caption=f"Мой профиль\n{'-'*25}\nИмя:" +
			f" {myprofile_data[0]}\nВозраст: {myprofile_data[1]}\nГород: {myprofile_data[2]}\nО себе: {myprofile_data[3]}")
			bot.send_message(chat_id=cid, text="Выберите действие", reply_markup=markup.gen_markup_myprofile())
	except Exception as ex:
		print('edit_myprofile:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "user_info")
def callback_edit_myprofile(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			db_cmd.upd_state_user(uid, "view_myprofile")
			myprofile_data = db_cmd.get_user_myprofile(uid)
			if myprofile_data[4] != '-':
				photo_id = f"{myprofile_data[4]}"
			else:
				photo_id = "AgACAgIAAxkBAAIEpWHxHvFZMAlLAmuluP1Nz-z_lugQAAIHuDEbBi6JSz10nVNPG1V-AQADAgADeAADIwQ"
			bot.send_photo(chat_id=cid, photo=photo_id, caption=f"Мой профиль\n{'-' * 25}\nИмя: {myprofile_data[0]}\nВозраст: {myprofile_data[1]}\nГород: {myprofile_data[2]}\nО себе: {myprofile_data[3]}")
			bot.send_message(chat_id=cid, text="Выберите действие", reply_markup=markup.gen_markup_myprofile())
	except Exception as ex:
		print('callback_edit_myprofile:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "edit_myprofile")
def callback_edit_myprofile(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			db_cmd.upd_state_user(uid, "edit_myprofile_name")
			bot.send_message(chat_id=cid, text="Введите Имя (оставьте поле пустым чтобы оставить текущее имя):")
	except Exception as ex:
		print('callback_edit_myprofile:', ex)


@bot.message_handler(content_types=["text"])
def edit_myprofile(message):
	cid = message.chat.id
	uid = message.from_user.id
	global myprofile_data
	try:
		if cid == uid and db_cmd.get_state_user(uid)[0] == "edit_myprofile_name":
			myprofile_data = [message.text.replace('*', '')]
			db_cmd.upd_state_user(uid, "edit_myprofile_age")
			bot.send_message(chat_id=cid, text="Введите Ваш возраст:")
		elif cid == uid and db_cmd.get_state_user(uid)[0] == "edit_myprofile_age":
			myprofile_data.append(message.text.replace('*', ''))
			db_cmd.upd_state_user(uid, "edit_myprofile_city")
			bot.send_message(chat_id=cid, text="Введите город:")
		elif cid == uid and db_cmd.get_state_user(uid)[0] == "edit_myprofile_city":
			myprofile_data.append(message.text.replace('*', ''))
			db_cmd.upd_state_user(uid, "edit_myprofile_about")
			bot.send_message(chat_id=cid, text="Введите данные о себе:")
		elif cid == uid and db_cmd.get_state_user(uid)[0] == "edit_myprofile_about":
			myprofile_data.append(message.text.replace('*', ''))
			bot.send_message(chat_id=cid, text="Для добавления фотографии профиля отправьте боту фото",
							 reply_markup=markup.gen_markup_confirm_myprofile())
			db_cmd.upd_state_user(uid, "edit_myprofile_photo")
	except Exception as ex:
		print('edit_myprofile:', ex)


@bot.message_handler(content_types=["photo"])
def add_photo(message):
	cid = message.chat.id
	uid = message.from_user.id
	try:
		if cid == uid:
			file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
			data = f'{myprofile_data[1]}*{myprofile_data[2]}*{myprofile_data[3]}*{file_info.file_id}'
			db_cmd.upd_user_myprofile(uid, myprofile_data[0], data)
			bot.send_message(chat_id=cid, text="Главное меню", reply_markup=markup.gen_markup_user())
			db_cmd.upd_state_user(uid, "main_menu")
	except Exception as ex:
		print('add_photo:', ex)


@bot.callback_query_handler(func=lambda call: call.data.endswith("confirm_myprofile_without_photo"))
def back_to_menu(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			data = f'{myprofile_data[1]}*{myprofile_data[2]}*{myprofile_data[3]}*-'
			db_cmd.upd_user_myprofile(uid, myprofile_data[0], data)
	except Exception as ex:
		print('back_to_menu:', ex)


@bot.callback_query_handler(func=lambda call: call.data.endswith("Back_to_menu"))
def back_to_menu(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid and call.data.startswith("admin"):
			db_cmd.upd_state_admin(uid, "menu_admin")
			bot.send_message(chat_id=cid, text="Меню администратора", reply_markup=markup.gen_markup_admin())
		elif cid == uid and call.data.startswith("user"):
			bot.send_message(chat_id=cid, text="Главное меню", reply_markup=markup.gen_markup_user())
	except Exception as ex:
		print('back_to_menu:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "activate_user")
def callback_activate_user(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		if cid == uid:
			db_cmd.upd_state_admin(uid, "activate_user")
			global list_users_inactive
			list_users_inactive = db_cmd.get_users_inactive()
			if len(list_users_inactive) > 0:
				bot.send_message(chat_id=cid, text="Список неактивных пользователей:",
								 reply_markup=markup.gen_markup_users_inactive(list_users_inactive))
			else:
				bot.send_message(chat_id=cid, text="Неактивные пользователи отсутствуют",
								 reply_markup=markup.gen_markup_users_inactive(list_users_inactive))
	except Exception as e:
		print('callback_activate_user:', e)

@bot.callback_query_handler(func=lambda call: call.data.startswith("activate_user:"))
def activate_users(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		user_to_activate_id = call.data.split(':')[1]
		if cid == uid and db_cmd.get_state_admin(uid)[0] == 'activate_user':
			if user_to_activate_id.lower() == 'all':
				bot.answer_callback_query(call.id, f'Все пользователи активированы')
				db_cmd.upd_state_inactive_users(tuple([i[0] for i in list_users_inactive]), "start")
			elif user_to_activate_id.lower() == 'back':
				pass
			else:
				bot.answer_callback_query(call.id, f'Пользователь с id: {user_to_activate_id} активирован')
				db_cmd.upd_state_inactive_users((int(user_to_activate_id),), "start")
	except Exception as ex:
		print('activate_users:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "delete_user")
def callback_delete_user(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		if cid == uid:
			db_cmd.upd_state_admin(uid, "delete_user")
			global list_users
			list_users = db_cmd.get_users_all()
			bot.send_message(chat_id=cid, text="Список пользователей:",
								 reply_markup=markup.gen_markup_users(list_users))
	except Exception as ex:
		print('callback_delete_user:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_user:"))
def delete_user(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		user_to_delete_id = call.data.split(':')[1]
		if cid == uid and db_cmd.get_state_admin(uid)[0] == 'delete_user':
			bot.answer_callback_query(call.id, f'Пользователь с id: {user_to_delete_id} удалён')
			db_cmd.delete_user(int(user_to_delete_id))
	except Exception as ex:
		print('delete_user:', ex)
'''

if __name__ == '__main__':
    bot.polling()
