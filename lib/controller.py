from datetime import datetime

from dao import dao
from lib import compare
from lib import parser

from lib.fileIO import FileIO
from lib.requestData import requestData


def get_today_locations(patient_seq):
    data = list(dao.get_patient_location_from_outdoor_log(patient_seq))

    result = []
    for val in data:
        result.append(val[0].split('/'))

    return result


# 금일 조도, 소음 평균값 DB 저장
# 시간에 따른 평균을 각각 구해야 할 것 같다.......
def insert_data_avg():
    # Delete all data int today_avg table.
    dao.del_all_data_today_avg()
    # 시간 값 추출 후 아침, 점심, 저녁, 밤, 환자번호로 구분
    outdoor_data = dao.get_outdoor_data()

    patient_cnt = 0
    day_time_data = [[[], [], [], []]]
    for i, val in enumerate(outdoor_data):
        if i is 0:
            day_time_data[patient_cnt].append(val[3])
            i += 1
        elif day_time_data[patient_cnt][4] is not val[3]:
            patient_cnt += 1
            day_time_data.append([[], [], [], []])
            day_time_data[patient_cnt].append(val[3])

        if day_time_data[patient_cnt][4] == val[3]:
            if 5 < val[2].time().hour < 12:
                day_time_data[patient_cnt][0].append(val)
            elif 11 < val[2].time().hour < 18:
                day_time_data[patient_cnt][1].append(val)
            elif 17 < val[2].time().hour < 22:
                day_time_data[patient_cnt][2].append(val)
            elif (21 < val[2].time().hour) or (val[2].time().hour < 6):
                day_time_data[patient_cnt][3].append(val)

    # day = [('95', '76', datetime.datetime(2019, 11, 5, 6, 30, 33), 37), ('95', '76', datetime.datetime......)]
    # val = ('95', '76', datetime.datetime(2019, 11, 5, 6, 30, 33), 37)
    # 아침, 점심, 저녁, 밤 데이터를 평균을 구한 후, insert to today_avg.
    for day_data in day_time_data:
        for i, day in enumerate(day_data):
            avg_list = [0, 0]
            val_cnt = 0
            patient_seq = 0
            day_time = 'MORNING'

            if type(day) is not int:
                for val in day:
                    avg_list[0] += int(val[0])
                    avg_list[1] += int(val[1])
                    val_cnt += 1
                    patient_seq = val[3]
                avg_list[0] = avg_list[0] / val_cnt
                avg_list[1] = avg_list[1] / val_cnt
                # day_data[i] = avg_list

                if i == 1:
                    day_time = 'LUNCH'
                elif i == 2:
                    day_time = 'DINNER'
                elif i == 3:
                    day_time = 'NIGHT'
                dao.set_today_avg(patient_seq, day_time, avg_list[0], avg_list[1])

    now = datetime.now()
    print('[%s-%s-%s %s:%s:%s]' % (now.year, now.month, now.day, now.hour, now.minute, now.second),
          ' insert_data_avg is done.')


# 1. 환자가 외출 상태일 때, 외부 센서의 데이터를 통하여 날씨등의 위험요소 판단 후 result 변수에 append
# 2. 전일 조도, 소음의 평균값을 조회하여 금일과 비교 후 result 변수에 merge 후 데이터 송신
# (미세먼지/초미세먼지, 강수량, 날씨, 기온)
def chk_all(data):
    location = compare.get_location(data['PatientSeq'], data['Location'])
    location_range = FileIO().read_location_info()
    result = []
    if (location_range['x'] <= location[0]) or (location_range['y'] <= location[1]):
        result.append(compare.dust_com(data))
        result.append(compare.pre_com(data))
        result.append(compare.sky_com(data))
        result.append(compare.temp_com(data))
    else:
        result.append(compare.illu_com(data))
        result.append(compare.noise_com(data))

    for msg in result:
        if msg is not None:
            obj = parser.make_requestObj('OutdoorSensing', msg, data['LogTime'], data['PatientSeq'])
            requestData().postData(obj)
