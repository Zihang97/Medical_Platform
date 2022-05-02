import pymysql

password = "root"


def create_table(password=password):
	# create a table for each user storing all messages sent and received
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = 'drop table if exists device'
	cursor.execute(sql)

	sql = 'create table device (username VARCHAR(40), type VARCHAR(20), measurement VARCHAR(20))'
	# type has to be one of Temperature, BloodPressure, Pulse, Oximeter, Weight, Height, Glucometer
	cursor.execute(sql)

	db.commit()
	db.close()


def insert_device(username, type, measurement, password=password):
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = 'insert into device (username, type, measurement) values(%s, %s, %s)'
	cursor.execute(sql, (username, type, measurement))

	db.commit()
	db.close()


def delete_device(username, type, password=password):
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = 'delete from device where username=%s and type=%s'
	cursor.execute(sql, (username, type))

	db.commit()
	db.close()


def get_device(username, password=password):
	db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

	cursor = db.cursor()

	sql = 'select * from device where username=%s'
	cursor.execute(sql, (username))
	results = cursor.fetchall()

	db.close()

	return results