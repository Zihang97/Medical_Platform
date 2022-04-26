import pymysql

password = "root"

def insertuser(username, pwd, password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = 'insert into user (username, password) values(%s, %s)'
	cursor.execute(sql, (username, pwd))

	db.commit()
	
	db.close()


def getusers(password=password):
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
