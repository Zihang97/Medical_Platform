import pymysql

password = "root"


def create_table(password=password):
    # create a table for each user storing all messages sent and received
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = 'drop table if exists mp_assignment'
    cursor.execute(sql)

    sql = 'create table mp_assignment (username VARCHAR(40), type VARCHAR(10), mp VARCHAR(40))'
    # type has to be one of None, Doctor and Nurse
    cursor.execute(sql)

    db.commit()
    db.close()


def insert_assignment(username, type, mp_name, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = 'insert into mp_assignment (username, type, mp) values(%s, %s, %s)'
    cursor.execute(sql, (username, type, mp_name))

    db.commit()
    db.close()


def delete_assignment(username, type, mp_name, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = 'delete from mp_assignment where username=%s and type=%s and mp=%s'
    cursor.execute(sql, (username, type, mp_name))

    db.commit()
    db.close()


def get_one_assignment(username, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = "select * from mp_assignment where username=%s"
    cursor.execute(sql, (username))
    results = cursor.fetchall()
    db.close()

    doctors = []
    nurses =[]
    for result in results:
        if result[1] == 'Doctor':
            doctors.append(result[2])
        else:
            nurses.append(result[2])

    return doctors, nurses


def get_patients(mp_name, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = "select * from mp_assignment where mp=%s"
    cursor.execute(sql, (mp_name))
    results = cursor.fetchall()
    db.close()

    patients = [result[0] for result in results]

    return patients


def get_all_assignments(password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = "select * from mp_assignment"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    return results
