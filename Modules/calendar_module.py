import pymysql
from datetime import datetime

password = "root"


def format_time(t):
    formatted_date = datetime.strptime(t, '%H:%M:%S')
    return formatted_date


def create_appointment_table(password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = 'drop table if exists appointment'
    cursor.execute(sql)

    sql = 'create table appointment (a_id INT AUTO_INCREMENT, doctor_name VARCHAR(20) NOT NULL, patient_name VARCHAR(20) NOT NULL,' \
          'appointment_date VARCHAR(40), start VARCHAR(40), finish VARCHAR(40), symptom TEXT, PRIMARY KEY (a_id)) '
    cursor.execute(sql)
    db.commit()
    db.close()


def store_appointment(doctor, patient, date, startime, endtime, symptom, password=password):
    t = (doctor, patient, date, startime, endtime, symptom)
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")
    cursor = db.cursor()

    # sql = '''insert into appointment (doctor_id, patient_id, appointment_date, start, finish) values (?,?,?,?,?)'''
    sql = 'insert into appointment (doctor_name, patient_name, appointment_date, start, finish, symptom) values (%s, %s, %s, %s, %s, %s)'
    # cursor.execute(sql, (doctor, patient, date, startime, endtime))
    cursor.execute(sql, t)
    db.commit()
    db.close()
    return cursor.lastrowid


def get_appointment(username, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()
    sql = 'select * from appointment where doctor_name = %s or patient_name = %s'
    cursor.execute(sql, (username, username))
    results = cursor.fetchall()
    db.commit()
    db.close()
    return results


def get_one_appointment(patient, doctor, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()
    sql = 'select * from appointment where doctor_name = %s and patient_name = %s'
    cursor.execute(sql, (doctor, patient))
    results = cursor.fetchall()
    db.commit()
    db.close()
    return results


def make_appointment(doctor, patient, date, startime, endtime, symptom, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")
    cursor = db.cursor()
    sql = "select * from appointment where doctor_name = %s or patient_name = %s"
    cursor.execute(sql, (doctor, patient))
    results = cursor.fetchall()
    # check available
    for entry in results:
        if (datetime.strptime(date, '%Y-%m-%d') - datetime.strptime(entry[3], '%Y-%m-%d')).days == 0:
            if format_time(str(entry[4])) <= format_time(startime) < format_time(str(entry[5])):
                print("Time conflict.")
                return
    store_appointment(doctor, patient, date, startime, endtime, symptom)

    db.commit()
    db.close()
    return cursor.lastrowid


def delete_one_appointment(doctor, patient, date, startime, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")
    cursor = db.cursor()

    sql = 'DELETE FROM appointment where doctor_name = %s and patient_name = %s and appointment_date = %s and start = %s'
    cursor.execute(sql, (doctor, patient, date, startime))

    db.commit()
    db.close()
    return cursor.lastrowid


def delete_appointment(username, date, startime, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")
    cursor = db.cursor()

    sql = 'DELETE FROM appointment where (doctor_name = %s or patient_name = %s) and appointment_date = %s and start = %s'
    cursor.execute(sql, (username, username, date, startime))

    db.commit()
    db.close()
    return cursor.lastrowid


def update_appointment(doctor, patient, date, startime, symptom, a_id, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")
    cursor = db.cursor()

    sql = 'UPDATE appointment SET doctor_name = %s and patient_name = %s and appointment_date = %s and start = %s and symptom = %s WHERE a_id = %s'
    cursor.execute(sql, (doctor, patient, date, startime, a_id))

    db.commit()
    db.close()
    return cursor.lastrowid


