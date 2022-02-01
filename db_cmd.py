import sqlite3


def create_tables():
	db_file = "db.db"
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS users(
						user_id INTEGER PRIMARY KEY NOT NULL,
						state TEXT NOT NULL,
						data TEXT NOT NULL)""")
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS Products(
						id INTEGER PRIMARY KEY NOT NULL,
						name TEXT NOT NULL,
						categors TEXT NOT NULL,
						price INTEGER NOT NULL,
						info TEXT NOT NULL,
						img TEXT)""")
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS cart(
						user_id INTEGER PRIMARY KEY NOT NULL,
						list_buy TEXT,
						amount TEXT)""")

def check_user_id(_user_id):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if not data:
			cur.close()
			add_user(_user_id)
			check = True
		else:
			cur.close()
	except Exception as ex:
		print("check_user_id", ex)
	finally:
		if conn is not None:
			conn.close()


def add_user(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""INSERT INTO users(user_id, state, data) VALUES(?, ?, ?);"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		mass = {'id':'', 'categor':'', 'name':'', 'price':''}
		cur.execute(sql, (_user_id,'start', str(mass)))
		conn.commit()
		cur.close()
	except Exception as ex:
		print('add_user:', ex)
	finally:
		if conn is not None:
			conn.close()

def get_categors():
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT categors FROM Products"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		lst_categor = []
		for i in data:
			lst_categor.append(i[0])
		lst_categor = list(set(lst_categor))
		cur.close()
	except Exception as ex:
		print('get_categors:', ex)
	finally:
		if conn is not None:
			conn.close()
		return lst_categor


def get_img_id(_id_product):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT img FROM Products WHERE id = {_id_product}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_img_id:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data[0]


def get_products(_categor):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM Products WHERE categors='{_categor}'"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		lst_product = []
		for i in data:
			lst_product.append(i)
		lst_product = list(set(lst_product))
		cur.close()
	except Exception as ex:
		print('get_products:', ex)
	finally:
		if conn is not None:
			conn.close()
		return lst_product


def get_info_product(_id_product):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM Products WHERE id={_id_product}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_info_product:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def up_data(_user_id, _data):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE users SET data="{_data}" WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_data:', ex)
	finally:
		if conn is not None:
			conn.close()


def get_data(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT data FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_data:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data[0]




'''
def check_user_id(_user_id, _name):
	# проверка наличия пользователя в базе, если нет - вызов функции добавления
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM users WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if not data:
			cur.close()
			add_user(_user_id, _name)
			check = True
		else:
			cur.close()
	except Exception as ex:
		print('check_user_id:', ex)
	finally:
		if conn is not None:
			conn.close()
	return check


def add_user(_user_id, _name):
	# добавление нового пользователя
	db_file = "db.db"
	conn = None
	try:
		sql = f"""INSERT INTO users(user_id, name, state, data) VALUES(?, ?, ?, ?);"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql, (_user_id, _name, 'inactive', '-*-*-*-'))
		conn.commit()
		cur.close()
	except Exception as ex:
		print('add_user:', ex)
	finally:
		if conn is not None:
			conn.close()


def check_admin(_user_id):
	# Проверка пользователя на права админа
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM admins WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if data is not None:
			check = True
		else:
			cur.close()
	except Exception as ex:
		print('check_admin:', ex)
	finally:
		if conn is not None:
			conn.close()
	return check


def check_user_state(_user_id):
	# Проверка активирован ли пользователь. True если да
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT state FROM users WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if data[0] != 'inactive':
			check = True
		else:
			cur.close()
	except Exception as ex:
		print('check_user_state:', ex)
	finally:
		if conn is not None:
			conn.close()
	return check


def get_users_inactive():
	# Достаем список неактивных юзеров для админа
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT user_id, name FROM users WHERE state LIKE '%inactive%'"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
	except Exception as ex:
		print('get_users_inactive:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_user_myprofile(_user_id):
	# Достаем информацию из профиля юзера
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT name, data FROM users WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_user_myprofile:', ex)
	finally:
		if conn is not None:
			conn.close()
		return (data[0],data[1].split('*')[0], data[1].split('*')[1], data[1].split('*')[2], data[1].split('*')[3])

# def get_user_data(_user_id):
# 	# Достаем информацию из профиля юзера для добавления фото/ Возможно уже не нужен!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 	db_file = "db.db"
# 	conn = None
# 	data = None
# 	try:
# 		sql = f"""SELECT data FROM users WHERE user_id = {_user_id}"""
# 		conn = sqlite3.connect(db_file)
# 		cur = conn.cursor()
# 		cur.execute(sql)
# 		data = cur.fetchone()
# 		cur.close()
# 	except Exception as ex:
# 		print('get_user_data:', ex)
# 	finally:
# 		if conn is not None:
# 			conn.close()
# 		return data



def get_users_all():
	# Список всех пользователей для анмина
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT user_id, name FROM users"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
	except Exception as ex:
		print('get_users_all:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def upd_state_admin(_user_id, _state):
	# Меняем состояние админа
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE admins SET state='{_state}' WHERE user_id={_user_id};"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_state_admin:', ex)
	finally:
		if conn is not None:
			conn.close()


def upd_state_user(_user_id, _state):
	# Меняем состояние юзера
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE users SET state='{_state}' WHERE user_id={_user_id};"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_state_user:', ex)
	finally:
		if conn is not None:
			conn.close()


def upd_user_myprofile(_user_id, _name, _data):
	# Меняем данные профиля юзера
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE users SET name='{_name}', data='{_data}' WHERE user_id={_user_id};"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_state_myprofile:', ex)
	finally:
		if conn is not None:
			conn.close()


# def upd_user_myprofile_data(_user_id, _data):
# 	# Меняем данные профиля юзера/ Возможно уже не нужен!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 	db_file = "db.db"
# 	conn = None
# 	try:
# 		sql = f"""UPDATE users SET data='{_data}' WHERE user_id={_user_id};"""
# 		conn = sqlite3.connect(db_file)
# 		cur = conn.cursor()
# 		cur.execute(sql)
# 		conn.commit()
# 		cur.close()
# 	except Exception as ex:
# 		print('up_state_myprofile_data:', ex)
# 	finally:
# 		if conn is not None:
# 			conn.close()


def get_state_admin(_user_id):
	# Считываем состояние админа
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT state FROM admins WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_state_admin:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_state_user(_user_id):
	# Считываем состояние юзера
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT state FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_state_user:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_name_user(_user_id):
	# Считываем имя юзера
	db_file = "db.db"
	conn = None
	data = None
	try:
		sql = f"""SELECT name FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_name_user:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def upd_state_inactive_users(_user_id, _state):
	# Меняем состояние юзера или нескольких
	# Используется при активации админом
	db_file = "db.db"
	conn = None
	if len(_user_id) == 1:
		_user_id = _user_id[0]
		sql = f"""UPDATE users SET state='{_state}' WHERE user_id={_user_id}"""
	else:
		sql = f"""UPDATE users SET state='{_state}' WHERE user_id IN {_user_id}"""
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print("upd_state_inactive_users:", ex)
	finally:
		if conn is not None:
			conn.close()


def delete_user(_user_id):
	# Удаление пользователя по ID
	db_file = "db.db"
	conn = None
	try:
		sql = f"""DELETE FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print("delete_user:", ex)
	finally:
		if conn is not None:
			conn.close()

'''
create_tables()
