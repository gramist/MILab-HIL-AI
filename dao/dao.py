import pymysql
from lib.fileIO import FileIO


def getConnection():
    db_info = FileIO().read_db_info('../conf/server.properties')

    return pymysql.connect(host=db_info['host'], port=int(db_info['port']), user=db_info['user'],
                           passwd=db_info['password'],
                           db=db_info['db'], charset=db_info['charset'], autocommit=True)


def get_data(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = "SELECT data FROM patient WHERE patient_num=%s"
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-SELECT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def set_data(patient_seq, data):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = "INSERT INTO patient(patient_num, data) VALUE (%s, %s)"
        cursor.execute(sql, (patient_seq, data))

        cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-INSERT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()


def del_data(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'DELETE FROM patient WHERE patient_num=%s AND idx NOT IN( SELECT * FROM (SELECT A.idx FROM patient A ' \
              'WHERE A.patient_num=%s ORDER BY A.idx desc limit 32)as tmp)'
        cursor.execute(sql, (patient_seq, patient_seq))

        cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()


def get_outdoor_data():
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'select illuminance, noise, log_time, patient_seq from w_outdoor_log where log_time between date_add(' \
              'curdate(), interval -1 day) and curdate()'
        cursor.execute(sql)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-SELECT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_patient_location(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'SELECT patient_location FROM W_PATIENT WHERE patient_seq=%s'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-SELECT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_patient_seq_from_outdoor_log():
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'select distinct patient_seq from w_outdoor_log where log_time between date_add(curdate(),' \
              ' interval -1 day) and curdate();'
        cursor.execute(sql)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-SELECT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def set_today_avg(patient_seq, day_time, illu, noise):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'insert into today_avg (patient_seq, day_time, illuminance, noise) value (%s, %s, %s, %s)'
        cursor.execute(sql, (patient_seq, day_time, illu, noise))

        cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-INSERT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()


def get_today_avg(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'select illuminance, noise, day_time from today_avg where patient_seq=%s;'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-INSERT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def del_all_data_today_avg():
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'delete from today_avg'
        cursor.execute(sql)

        cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()


def run_sql_hard_code(sql):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        cursor.execute(sql)

        data = cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-SELECT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return True
