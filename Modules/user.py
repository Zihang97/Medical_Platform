import pymysql

password = "root"


def create_table(password=password):
	# create a table for each user storing all messages sent and received
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = 'drop table if exists user'
	cursor.execute(sql)

	sql = 'create table user (username VARCHAR(40), password VARCHAR(40), email VARCHAR(40), ' \
		  'age VARCHAR(10), gender VARCHAR(10), dob VARCHAR(40))'
	# username has to be unique
	cursor.execute(sql)

	db.commit()
	db.close()


def insert_user(username, pwd, email, age, gender, dob, password=password):
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")
	 
	cursor = db.cursor()

	sql = 'insert into user (username, password, email, age, gender, dob) ' \
		  'values(%s, %s, %s, %s, %s, %s)'
	cursor.execute(sql, (username, pwd, email, age, gender, dob))

	db.commit()
	db.close()


def delete_user(username, password=password):
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = 'delete from user where username=%s'
	cursor.execute(sql, (username))

	db.commit()
	db.close()


def get_users_password(password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = "select * from user"
	cursor.execute(sql)
	results = cursor.fetchall()
	
	users = {}
	for row in results:
		users[row[0]] = row[1]
	 
	db.close()

	return users


def get_one_user(username, password=password):
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = "select * from user where username=%s"
	cursor.execute(sql, (username))
	result = cursor.fetchone()

	return result


def get_all_users(password=password):
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = "select * from user"
	cursor.execute(sql)
	results = cursor.fetchall()

	return results
