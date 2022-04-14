import pymysql
from datetime import datetime

password = "****"

def current_time():
	# get current time and transfer it into format accepted by mysql
	now = datetime.now()
	formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
	return formatted_date

def create_table(username, password = password):
	# create a table for each user storing all messages sent and received
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	tablename = 'chat_' + username

	sql = 'drop table if exists ' + tablename
	cursor.execute(sql)

	sql = 'create table ' + tablename + ' (connecting_user VARCHAR(40), message_type VARCHAR(10), content TEXT, status VARCHAR(10), time DATETIME)'
	# message_type has to be one of TEXT, VIDEO and VOICE, status is either Sent or Received
	cursor.execute(sql)

	db.commit()
	 
	db.close()


def store_message(username, connecting_user, message_type, content, status, time, password = password):
	# store message into chat table belong to that user
	tablename = 'chat_' + username

	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()
	
	sql = 'insert into ' + tablename + ' (connecting_user, message_type, content, status, time) values(%s, %s, %s, %s, %s)'
	cursor.execute(sql, (connecting_user, message_type, content, status, time))

	db.commit()
	
	db.close()


def get_messages(username, connecting_user, password = password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()
	tablename = 'chat_' + username

	sql = "select * from " + tablename + " where connecting_user=%s"
	cursor.execute(sql, (connecting_user))
	results = cursor.fetchall()
	 
	db.close()

	return results


