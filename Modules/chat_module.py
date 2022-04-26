import pymysql
from datetime import datetime

password = "root"

def current_time():
	# get current time and transfer it into format accepted by mysql
	now = datetime.now()
	formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
	return formatted_date


def create_table(password = password):
	# create a table for each user storing all messages sent and received
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = 'drop table if exists chat'
	cursor.execute(sql)

	sql = 'create table chat (sender VARCHAR(40), recipient VARCHAR(40), message_type VARCHAR(10), content TEXT, time DATETIME)'
	# message_type has to be one of TEXT, VIDEO and VOICE
	cursor.execute(sql)

	db.commit() 
	db.close()


def store_message(sender, recipient, message_type, content, time, password = password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()
	
	sql = 'insert into chat (sender, recipient, message_type, content, time) values(%s, %s, %s, %s, %s)'
	cursor.execute(sql, (sender, recipient, message_type, content, time))

	db.commit()
	db.close()


def get_messages(sender, recipient, password = password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = "select * from chat where (sender=%s and recipient=%s) or (sender=%s and recipient=%s)"
	cursor.execute(sql, (sender, recipient, recipient, sender))
	results = cursor.fetchall()
	 
	db.close()

	return results



