import pymysql
from datetime import datetime

password = "root"


def create_appointment_table(password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()

    sql = 'drop table if exists appointment'
    cursor.execute(sql)

    sql = 'create table appointment (doctor_name VARCHAR(20), patient_name VARCHAR(20), appointment_date VARCHAR(40), ' \
          'start VARCHAR(40), symptom TEXT) '
    cursor.execute(sql)
    db.commit()
    db.close()


def insert_appointment(doctor, patient, date, startime, symptom, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")
    cursor = db.cursor()

    # sql = '''insert into appointment (doctor_id, patient_id, appointment_date, start, finish) values (?,?,?,?,?)'''
    sql = 'insert into appointment (doctor_name, patient_name, appointment_date, start, symptom) values (%s, %s, %s, %s, %s)'
    # cursor.execute(sql, (doctor, patient, date, startime, endtime))
    cursor.execute(sql, (doctor, patient, date, startime, symptom))
    db.commit()
    db.close()


def get_doctor_appointment(doctor_name, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()
    sql = 'select * from appointment where doctor_name = %s'
    cursor.execute(sql, (doctor_name))
    results = cursor.fetchall()
    db.commit()
    db.close()
    return results

def get_patient_appointment(patient_name, password=password):
    db = pymysql.connect(host="localhost", user="root", password=password, database="medical_platform")

    cursor = db.cursor()
    sql = 'select * from appointment where patient_name = %s'
    cursor.execute(sql, (patient_name))
    results = cursor.fetchall()
    db.commit()
    db.close()
    return results
