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
						list_buy TEXT NOT NULL,
						amount INTEGER NOT NULL,
						active INTEGER NOT NULL)""")
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS admins(
						user_id INTEGER PRIMARY KEY NOT NULL,
						state TEXT NOT NULL,
						data TEXT)""")
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


def check_user_is_admin(_user_id):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM admins WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if data is not None:
			cur.close()
			check = True
		else:
			cur.close()
	except Exception as ex:
		print("check_user_is_admin", ex)
	finally:
		if conn is not None:
			conn.close()
		return check


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


def get_cart(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM cart WHERE user_id = {_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_cart:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def set_cart(_user_id, _lst_id_product, _amount):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""INSERT INTO cart(user_id,list_buy,amount,active) VALUES(?,?,?,?)"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql, (_user_id, _lst_id_product, _amount, '0'))
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_cart:', ex)
	finally:
		if conn is not None:
			conn.close()

def up_cart(_user_id, _lst_id_product, _amount):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE cart SET list_buy="{_lst_id_product}",
								   amount={_amount} 
								   WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_cart:', ex)
	finally:
		if conn is not None:
			conn.close()



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


create_tables()
