import json
import pymysql
from lib.fileIO import FileIO


def getConnection():
    db_info = FileIO().read_db_info('../conf/server.properties')

    return pymysql.connect(host=db_info['host'], port=int(db_info['port']), user=db_info['user'],
                           passwd=db_info['password'],
                           db=db_info['db'], charset=db_info['charset'], autocommit=True)


def get_data(patient_num):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = "SELECT data FROM patient WHERE patient_num=%s"
        cursor.execute(sql, patient_num)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-SELECT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def set_data(patient_num, data):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = "INSERT INTO patient(patient_num, data) VALUE (%s, %s)"
        cursor.execute(sql, (patient_num, data))

        data = cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-INSERT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()


def del_data(patient_num):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'DELETE FROM patient WHERE patient_num=%s AND idx NOT IN( SELECT * FROM (SELECT A.idx FROM patient A ' \
              'WHERE A.patient_num=%s ORDER BY A.idx desc limit 32)as tmp); '
        cursor.execute(sql, (patient_num, patient_num))

        data = cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()
