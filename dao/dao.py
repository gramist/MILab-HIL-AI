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
        sql = "SELECT data FROM Patient WHERE patient_num=%s"
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
        sql = "INSERT INTO Patient(patient_num, data) VALUE (%s, %s)"
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
        sql = 'DELETE FROM Patient WHERE patient_num=%s AND idx NOT IN( SELECT * FROM (SELECT A.idx FROM Patient A ' \
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
        sql = 'select ILLUMINANCE, NOISE, LOG_TIME, PATIENT_SEQ from W_OUTDOOR_LOG where LOG_TIME between date_add(' \
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
        sql = 'SELECT PATIENT_LOCATION FROM W_PATIENT WHERE PATIENT_SEQ=%s'
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
        sql = 'select distinct PATIENT_SEQ from W_OUTDOOR_LOG where LOG_TIME between date_add(curdate(),' \
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
        sql = 'select LOCATION from W_OUTDOOR_LOG where PATIENT_SEQ=%s and date_format(' \
              'LOG_TIME, "%%Y-%%m-%%d")=curdate() '
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
        sql = 'insert into Today_Avg (patient_seq, day_time, illuminance, noise) value (%s, %s, %s, %s)'
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
        sql = 'select illuminance, noise, day_time from Today_Avg where patient_seq=%s;'
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
        sql = 'delete from Today_Avg'
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
        sql = 'SELECT LOG_TIME, CONTENT from AbnormalBehavior where PATIENT_SEQ=%s order by LOG_TIME'
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
        sql = 'SELECT time, content from Today_Schedule where patient_seq=%s order by log_time'
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
        sql = 'insert into  Today_Schedule(patient_seq, time, content) value (%s, %s, %s)'
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
        sql = 'delete from Today_Schedule where patient_seq=%s'
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
        sql = 'SELECT LOG_TIME, CONTENT from PastSchedule where PATIENT_SEQ=%s order by LOG_TIME'
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
        sql = 'SELECT SENSOR_LOG_TIME, SENSOR_CODE from W_SENSOR_LOG where PATIENT_SEQ=%s and ' \
              'CREATED_TIME > curdate() order by SENSOR_LOG_TIME;'
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
        sql = 'select distinct PATIENT_SEQ from W_SENSOR_LOG where CREATED_TIME > curdate()'
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
        sql = 'select SENSOR_CODE from W_SENSOR_LOG where (SENSOR_LOG_TIME between %s and %s ) and PATIENT_SEQ=%s'
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
