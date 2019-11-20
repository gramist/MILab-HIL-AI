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


def get_patient_location_from_outdoor_log(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'select location from w_outdoor_log where patient_seq=%s and date_format(' \
              'log_time, "%%Y-%%m-%%d")=curdate() '
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


def get_abnormal_behavior(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'SELECT log_time, content from AbnormalBehavior where patient_seq=%s order by log_time'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_abnormal_week(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'SELECT content from AbnormalBehavior where patient_seq=%s and log_time between date_add(' \
              'now(), interval -1 week) and now() order by log_time'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_outdoor_sensing(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'SELECT log_time, content from OutdoorSensing where patient_seq=%s order by log_time'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_today_schedule(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'SELECT time, content from today_schedule where patient_seq=%s order by log_time'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def set_today_schedule(patient_seq, time, content):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'insert into  today_schedule(patient_seq, time, content) value (%s, %s, %s)'
        cursor.execute(sql, (patient_seq, time, content))

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()


def del_today_schedule(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'delete from today_schedule where patient_seq=%s'
        cursor.execute(sql, patient_seq)

        cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)
        return False

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return True


def get_past_schedule(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'SELECT log_time, content from PastSchedule where patient_seq=%s order by log_time'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_w_sensor(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'SELECT sensor_log_time, sensor_idk from w_sensor_log where patient_seq=%s and ' \
              'created_time > curdate() order by sensor_log_time;'
        cursor.execute(sql, patient_seq)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_w_sensor_patient_seq():
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'select distinct patient_seq from w_sensor_log where created_time > curdate()'
        cursor.execute(sql)

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def get_w_sensor_idk_time(time1, time2, patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = 'select sensor_idk from w_sensor_log where (sensor_log_time between %s and %s ) and patient_seq=%s'
        cursor.execute(sql, (time1, time2, patient_seq))

        data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data


def run_sql_hard_code(sql):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        cursor.execute(sql)

        cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-SELECT ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return True
