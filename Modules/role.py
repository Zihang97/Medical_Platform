import pymysql

password = "root"

def create_table(password = password):
	# create a table for role
	# each user can have multiple roles
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = 'drop table if exists role'
	cursor.execute(sql)

	sql = 'create table role (username VARCHAR(40), role VARCHAR(40))'
	# role has to be one of None, Admin, Nurse, Doctor, Patient and Family
	cursor.execute(sql)

	db.commit() 
	db.close()


def add_role(username, role, password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = 'insert into role (username, role) values(%s, %s)'
	cursor.execute(sql, (username, role))

	db.commit()
	db.close()


def update_role(username, ori_role, new_role, password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = 'update role set role=%s where username=%s and role=%s'
	cursor.execute(sql, (new_role, username, ori_role))

	db.commit()
	db.close()


def delete_role(username, role, password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = 'delete from role where username=%s and role=%s'
	cursor.execute(sql, (username, role))

	db.commit()
	db.close()


def get_roles(password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "medical_platform")
	 
	cursor = db.cursor()

	sql = "select * from role"
	cursor.execute(sql)
	results = cursor.fetchall()
	
	user_roles = {}
	for row in results:
		if row[0] in user_roles:
			user_roles[row[0]].append(row[1])
		else:
			user_roles[row[0]] = [row[1]]
	 
	db.close()
	return user_roles


