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
        sql = 'SELECT PATIENT_LOCATION_ORIGIN FROM W_PATIENT WHERE PATIENT_SEQ=%s'
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
        sql = 'select LOCATION_ORIGIN from W_OUTDOOR_LOG where PATIENT_SEQ=%s and date_format(' \
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

# Guideline DML START
def get_guide_opinion(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
            SELECT /* 관찰 의견 */
	            WP.PATIENT_SEQ AS PATIENT_SEQ
                , WPO.CONDITION_SEQ
	            , WPO.OPINION_TEXT
            FROM W_PATIENT WP, W_PATIENT_OPINION WPO
            WHERE
	            WP.PATIENT_SEQ = %s
	            AND WP.PATIENT_SEQ = WPO.PATIENT_SEQ 
            ORDER BY CONDITION_SEQ DESC
            LIMIT 1 '''
        cursor.execute(sql, patient_seq)

        data = cursor.fetchone()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_cognicon_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
            SELECT /* 인지기능 상태 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPC.CONDITION_SEQ 
            , WPC.YEAR_SCORE + WPC.MONTH_SCORE + WPC.DAY_SCORE + WPC.WEEK_SCORE + WPC.SEASON_SCORE 
            + WPC.COUNTRY_SCORE + WPC.CITY_SCORE + WPC.WHAT_SCORE + WPC.WHERE_SCORE + WPC.FLOOR_SCORE 
            + WPC.MEMORY1_SCORE + WPC.MEMORY2_SCORE + WPC.MEMORY3_SCORE + WPC.CONCENT1_SCORE + WPC.CONCENT2_SCORE 
            + WPC.CONCENT3_SCORE + WPC.CONCENT4_SCORE + WPC.CONCENT5_SCORE + WPC.REMIND1_SCORE + WPC.REMIND2_SCORE 
            + WPC.REMIND3_SCORE + WPC.CALLNAME1_SCORE + WPC.CALLNAME2_SCORE + WPC.COMMAND1_SCORE + WPC.COMMAND2_SCORE 
            + WPC.COMMAND3_SCORE + WPC.AFTERSPEAK_SCORE + WPC.PENTAGON_SCORE + WPC.READ_SCORE + WPC.WRITE_SCORE + WPC.EDULEVEL_SCORE
            AS COGNICON_SCORE 
            , DATE_FORMAT(WPC.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP, W_PATIENT_COGNICON WPC
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPC.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()
    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_fallcon_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 낙상 위험도 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPF.CONDITION_SEQ 
            , WPF.TOTAL_SCORE AS FALLCON_SCORE
            , DATE_FORMAT(WPF.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
            , (CASE
                WHEN WPF.TOTAL_SCORE <= 4
                THEN '낮음'
                WHEN WPF.TOTAL_SCORE >= 5 AND WPF.TOTAL_SCORE <= 10
                THEN '높음'
                ELSE '아주 높음'
                END) AS fc_rs
        FROM W_PATIENT WP, W_PATIENT_FALLCON WPF
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPF.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_decub_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 욕창 위험도 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPD.CONDITION_SEQ 
            , WPD.TOTAL_SCORE AS DECUB_SCORE
            , DATE_FORMAT(WPD.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
            , (CASE
                WHEN WPD.TOTAL_SCORE >= 19 AND WPD.TOTAL_SCORE >= 23
                THEN '위험 없음'
                WHEN WPD.TOTAL_SCORE >= 13 AND WPD.TOTAL_SCORE <= 18
                THEN '위험 있음'
                ELSE '위험 높음'
                END) AS dc_rs
        FROM W_PATIENT WP, W_PATIENT_DECUBITUSICON WPD
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPD.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_bloodsugar(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 혈당 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPH.CONDITION_SEQ 
            , WPH.MEAL_YN
            , WPH.BLOODSUGAR_SCORE
            , (CASE
                WHEN (WPH.MEAL_YN = 0 AND WPH.BLOODSUGAR_SCORE >= 70 AND WPH.BLOODSUGAR_SCORE <= 99)
                    OR (WPH.MEAL_YN = 1 AND WPH.BLOODSUGAR_SCORE < 140)
                THEN '정상'
                ELSE '관찰 필요'
                END) AS bs_rs
            , DATE_FORMAT(WPH.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP, W_PATIENT_HEALTHCON WPH
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_bloodpress(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 혈압 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPH.CONDITION_SEQ 
            , WPH.BLOODPRESSUREH_SCORE 
            , WPH.BLOODPRESSUREL_SCORE
            , (CASE
                WHEN WPH.BLOODPRESSUREH_SCORE < 120 AND BLOODPRESSUREL_SCORE < 80
                THEN '정상'
                ELSE '관찰 필요'
                END) AS bp_rs
            , DATE_FORMAT(WPH.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP, W_PATIENT_HEALTHCON WPH
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

# def get_debu_yn(patient_seq):
#     try:
#         conn = getConnection()
#
#         cursor = conn.cursor()
#         sql = '''
#         SELECT /* 욕창발생여부 */
#             WP.PATIENT_SEQ AS PATIENT_SEQ
#             , WPH.CONDITION_SEQ
#             , WPH.DEBU_YN
#         FROM W_PATIENT WP, W_PATIENT_HEALTHCON WPH
#         WHERE
#             WP.PATIENT_SEQ = %s
#             AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ
#         ORDER BY CONDITION_SEQ DESC
#         LIMIT 1 '''
#         cursor.execute(sql, patient_seq)
#
#         data = cursor.fetchone()
#
#     except Exception as e:
#         conn.rollback()
#         print('[SQL-DELETE ERROR] : ', e)
#
#     finally:
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#     return data

def get_scratch_yn(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
         SELECT /* 상처발생여부 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPH.CONDITION_SEQ 
            , WPH.SCRATCH_YN
            , DATE_FORMAT(WPH.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP, W_PATIENT_HEALTHCON WPH
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_bodycon_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 신체 상태 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPB.CONDITION_SEQ
            , WPB.BODYCON_ITEM1_SCORE + WPB.BODYCON_ITEM2_SCORE + WPB.BODYCON_ITEM3_SCORE + WPB.BODYCON_ITEM4_SCORE
              + WPB.BODYCON_ITEM5_SCORE + WPB.BODYCON_ITEM6_SCORE + WPB.BODYCON_ITEM7_SCORE + WPB.BODYCON_ITEM8_SCORE
              + WPB.BODYCON_ITEM9_SCORE + WPB.BODYCON_ITEM10_SCORE + WPB.BODYCON_ITEM11_SCORE + WPB.BODYCON_ITEM12_SCORE
            AS BODY_SCORE
            , DATE_FORMAT(WPB.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP, W_PATIENT_BODYCON WPB
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPB.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else :
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_clean_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 청결 상태 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPC.CONDITION_SEQ
            , WPC.UPPER_CLEAN + WPC.LOWER_CLEAN + WPC.ARM_CLEAN + WPC.LEG_CLEAN + WPC.HEAD_CLEAN
            AS CLEAN_SCORE
            , WPC.CREATED_TIME
        FROM W_PATIENT WP, W_PATIENT_CLEANCON WPC
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPC.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_hearing_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 청취 능력 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPH.CONDITION_SEQ 
            , WPH.HEARING_SCORE
            , DATE_FORMAT(WPH.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP,  W_PATIENT_HEALTHCON WPH
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_comm_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 의사 소통 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPH.CONDITION_SEQ 
            , WPH.COMM_SCORE
            , DATE_FORMAT(WPH.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP,  W_PATIENT_HEALTHCON WPH
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_pron_score(patient_seq, limit='limit 1'):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT /* 발음 능력 */
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPH.CONDITION_SEQ 
            , WPH.PRON_SCORE
            , DATE_FORMAT(WPH.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP,  W_PATIENT_HEALTHCON WPH
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        ''' + limit
        cursor.execute(sql, patient_seq)

        if limit != '':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

    except Exception as e:
        conn.rollback()
        print('[SQL-DELETE ERROR] : ', e)

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return data

def get_health_info(patient_seq):
    try:
        conn = getConnection()

        cursor = conn.cursor()
        sql = '''
        SELECT 
            WP.PATIENT_SEQ AS PATIENT_SEQ 
            , WPH.CONDITION_SEQ
            /* 혈압 */ 
            , COALESCE(WPH.BLOODPRESSUREH_SCORE,'-') AS BLOODPRESSUREH_SCORE
            , COALESCE(WPH.BLOODPRESSUREL_SCORE,'-') AS BLOODPRESSUREL_SCORE
            /* 혈당 */
            , (CASE WPH.MEAL_YN
                WHEN 0 THEN 
                '식전'
                ELSE
                '식후'
                END) AS MEAL_YN
            , COALESCE(WPH.BLOODSUGAR_SCORE,'-') AS BLOODSUGAR_SCORE
            /* 청취 능력 */
            , COALESCE(WPH.HEARING_SCORE,'-') AS HEARING_SCORE
            /* 의사소통 */
            , COALESCE(WPH.COMM_SCORE,'-') AS COMM_SCORE
            /* 발음능력 */
            , COALESCE(WPH.PRON_SCORE,'-') AS PRON_SCORE
            /* 욕창 발생여부 */ 
            , (CASE WPH.DEBU_YN WHEN 1 THEN 'Y' ELSE 'N' END) AS DEBU_YN
            /* 상처 발생여부 */ 
            , (CASE WPH.SCRATCH_YN WHEN 1 THEN 'Y' ELSE 'N' END) AS SCRATCH_YN
            , DATE_FORMAT(WPH.CREATED_TIME, '%%Y-%%m-%%d') AS CREATED_TIME
        FROM W_PATIENT WP, W_PATIENT_HEALTHCON WPH
        WHERE
            WP.PATIENT_SEQ = %s
            AND WP.PATIENT_SEQ = WPH.PATIENT_SEQ 
        ORDER BY CONDITION_SEQ DESC
        '''
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
