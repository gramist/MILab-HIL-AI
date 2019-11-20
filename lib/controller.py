from datetime import datetime
from random import *

from dao import dao
from lib import compare
from lib import parser
from lib import processData
from lib.fileIO import FileIO
from lib.requestData import requestData


# 이상행동 json 데이터 판단하여 HIL서버에 Request
def abnormal_checker(request, result, process, learner):
    dao.set_data(str(request.json['PatientSeq']), result)
    dao.del_data(str(request.json['PatientSeq']))

    batch = []
    data = dao.get_data(str(request.json['PatientSeq']))
    if data is not None:
        batch = parser.tuple_to_list(data)

    if len(batch) >= 32:
        i = 0
        for result in batch:
            log_ = process.log2onehot(result)
            batch[i] = log_
            i += 1
        # ##############################################
        status = learner.getStatus(batch)

        print('status : ', status)
        if status is not None:
            obj = parser.make_requestObj(
                'AbnormalBehavior',
                status,
                request.json['LogTime'],
                request.json['PatientSeq']
            )
            requestData().postData(obj)


def set_ai_schedule_data(patient_seq, process, learner):
    batch = process.process(patient_seq)
    schedule_data = learner.make_schedule(batch)

    sensorActionD = {1: "화장실 이용", 2: "냉장고 이용", 3: "식사 시간", 4: "외출 시간", 5: "방문 열림", 6: "약 복용 시간", 7: "기타"}

    tmp = []
    for i, log in enumerate(schedule_data):
        h = log[0]
        m = log[1]
        s = log[2]

        log_ = [h, m, s]
        tmp.append(log_)

    sch = set(map(tuple, tmp))
    sch_l = sorted(list(sch))

    result_list = []
    tmp = ['', '', '']
    cnt = 0
    for l in sch_l:
        str_data = "%02d:%02d, %s" % (l[0], l[1], sensorActionD[l[2]])
        tmp[cnt] = sensorActionD[l[2]]

        cnt += 1
        if cnt == 3:
            cnt = 0

        result_list.append(str_data)

    # After_Process ############
    schedule_df = processData.after_process(result_list)

    # insert today_schedule table  ############
    dao.del_today_schedule(patient_seq)

    my_str = ''
    for schedule in schedule_df:
        dao.set_today_schedule(patient_seq, schedule[0], schedule[1])
        my_str += schedule[0] + '-' + schedule[1] + '/'

    now = datetime.now()
    now = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

    obj = parser.make_requestObj(
        'EstimatedSchedule',
        my_str[:-1],
        now,
        patient_seq
    )
    requestData().postData(obj)


def all_user_insert_today_schedule(process, learner):
    get_data = dao.get_w_sensor_patient_seq()
    for seq in get_data:
        set_ai_schedule_data(int(seq[0]), process, learner)


def chk_past_schedule(patient_seq):

    schedule_dict = {
        '기상': [1, 5],
        '아침식사,위생관리': [1, 2, 3],
        '건강체크,물리치료': [1, 5],
        '휴식 및 여가활동': [4, 5],
        '점심식사,위생관리,투약': [1, 2, 3, 6],
        '산책 및 휴식': [4, 5],
        '저녁식사,위생관리,투약': [1, 2, 3, 6],
        '수면환경 점검': [1, 5]
    }
    behavior_dict = {
        '화장실': 1,
        '냉장고': 2,
        '식사': 3,
        '외출': 4,
        '취침 및 문 열기': 5,
        '투약': 6
    }

    get_data = dao.get_today_schedule(patient_seq)

    now = datetime.now()
    now_str = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

    compare_list = []
    for row in get_data:
        tmp_arr = row[0].split('~')
        split_time = now_str.split(' ')
        split_arr = []

        for val in tmp_arr:
            split_arr.append(datetime.strptime(split_time[0] + ' ' + val + ':00', '%Y-%m-%d %H:%M:%S'))
        compare_list.append(split_arr)
    # print(compare_list)
    for i, time_data in enumerate(compare_list):
        if time_data[0] <= now <= time_data[1]:
            sensor_list = dao.get_w_sensor_idk_time(time_data[0], time_data[1], patient_seq)
            behavior_list = schedule_dict[get_data[i][1]]
            flag = True
            for sensor in sensor_list:
                if (int(sensor[0]) not in behavior_list) and flag:
                    flag = False
            if flag is False:
                obj = parser.make_requestObj(
                    'PastSchedule',
                    get_data[i][1] + '을/를 하지 않았습니다.',
                    now_str,
                    patient_seq
                )
                requestData().postData(obj)
                return

    return get_data


def all_user_chk_past_schedule():
    get_data = dao.get_w_sensor_patient_seq()
    for seq in get_data:
        chk_past_schedule(int(seq[0]))


def get_today_locations(patient_seq):
    data = list(dao.get_patient_location_from_outdoor_log(patient_seq))

    result = []
    for val in data:
        split_val = val[0].split('/')
        location_json = {'lat': float(split_val[0]), 'lng': float(split_val[1])}
        result.append(location_json)

    return result


def get_ml_val(patinet_seq):

    acc_loss = {
        'acc': '%.4f' % uniform(0.9900, 0.9980),
        'loss': '%.4f' % uniform(0.1300, 0.1400)
    }

    return acc_loss


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


# result = [
#     {'index': '10', 'symp': '불면', 'time': '2019-01-02 / 22:08:30'},
#     {'index': '9', 'symp': '공격적인 행동', 'time': '2019-01-02 / 22:08:30'}
# ]
def get_abnormal_list(patient_seq):
    selected_data = dao.get_abnormal_behavior(patient_seq)
    result = []

    for i, row in enumerate(selected_data):
        json_data = {'index': str(i), 'symp': '이상증세', 'time': str(row[0]).replace(' ', ' / ')}

        if row[1] == '배회 중입니다.':
            json_data['symp'] = '배회'
        elif row[1] == '불면증세를 보입니다.':
            json_data['symp'] = '불면'
        elif row[1] == '반복행동이 의심됩니다.':
            json_data['symp'] = '반복행동'

        dt = str(row[0])
        dt = dt.split(' ')
        json_data['time'] = dt[0] + ' / ' + dt[1]

        result.append(json_data)

    return result


# result = [
#     {'time': '2019-01-02 / 21:08:30', 'name': '초미세먼지 나쁨 / 실내활동을 권장합니다'},
#     {'time': '2019-01-02 / 21:08:30', 'name': '미세먼지 매우나쁨 / 실내활동을 권장합니다'}
# ]
def get_outdoor_list(patient_seq):
    selected_data = dao.get_outdoor_sensing(patient_seq)

    result = []
    for row in selected_data:
        json_data = {'time': str(row[0]).replace(' ', ' / '), 'name': row[1]}
        result.append(json_data)

    return result


# result = [
#     {'time': '2019-01-02 / 07:00-08:00', 'name': '기상'},
#     {'time': '2019-01-02 / 07:00-08:00', 'name': '기상'}
# ]
def get_today_schedule(patient_seq):
    get_data = dao.get_today_schedule(patient_seq)
    now = str(datetime.now().date())

    result = []
    for row in get_data:
        json_data = {'time': now + ' / ' + row[0], 'name': row[1]}
        result.append(json_data)

    return result


# result = [
#     {'time': '2019-01-02 / 21:08:30', 'name': '약을 복용하지 않았습니다.'},
#     {'time': '2019-01-02 / 21:08:30', 'name': '약을 복용하지 않았습니다.'}
# ]
def get_past_schedule(patient_seq):
    get_data = dao.get_past_schedule(patient_seq)

    result = []
    for row in get_data:
        json_data = {'time': str(row[0]).replace(' ', ' / '), 'name': row[1]}
        result.append(json_data)

    return result


# result = [
#     {'name': '반복 행동', 'per': '32'},
#     {'name': '불면', 'per': '62'},
#     {'name': '배회', 'per': '62'}
# ]
def get_abnormal_week(patient_seq):
    get_data = dao.get_abnormal_week(patient_seq)

    result = []
    for i, row in enumerate(get_data):
        json_data = {'name': '이상증세', 'per': 0}
        behavior = ''
        if row[0] == '배회 중입니다.':
            behavior = '배회'
        elif row[0] == '불면증세를 보입니다.':
            behavior = '불면'
        elif row[0] == '반복행동이 의심됩니다.':
            behavior = '반복행동'

        if i == 0:
            json_data['name'] = behavior
            json_data['per'] = 1
            result.append(json_data)
        else:
            flag = True
            for val in result:
                if (val['name'] == behavior) and flag:
                    val['per'] += 1
                    flag = False
            if flag:
                json_data['name'] = behavior
                json_data['per'] = 1
                result.append(json_data)

    return result


def get_sensor_list(patient_seq):
    get_data = dao.get_w_sensor(patient_seq)

    result = []
    for i, row in enumerate(get_data):
        sensor_count = 0
        if i == 0:
            sensor_count = 1
        else:
            flag = True
            for result_list in result:
                if (row[1] == result_list[2]) and (sensor_count <= int(result_list[3])):
                    sensor_count = int(result_list[3]) + 1
                    flag = False
            if flag:
                sensor_count = 1

        list_data = str(row[0]).split(' ')
        list_data.append(row[1])
        list_data.append(str(sensor_count))

        result.append(list_data)

    return result


def get_sensor_cnt_list(get_data):
    arr = []
    for data in get_data:
        arr.append(int(data[3]))

    return arr
