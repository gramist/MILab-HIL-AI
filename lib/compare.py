from dao import dao
from lib import parser
from lib.fileIO import FileIO
from lib.requestData import requestData


# data = {
#     'PacketType': 'OutdoorLog',
#     'PatientSeq': 37,
#     'Precipitation': 4,
#     'Sky': 4,
#     'Illuminance': 32,
#     'Temperatures': 10.2,
#     'Finedust': 1,
#     'UltraFinedust': 2,
#     'Noise': 73,
#     'Location': '37.755430/127.036502',
#     'LogTime': '2019-08-25 1:16:30'
# }


# 환자의 집과 실제 위치를 비교하여 외출 상태임을 판단
def get_location(patientSeq, location):
    # 원본은 ('37.755430/127.036502',)이런식으로 받아온다. 따라서 [0]번째 value를 받아와서 자른다. (좀 하드코딩 부분이라..)
    p_loc = dao.get_patient_location(patientSeq)[0]
    p_loc = p_loc.split('/')
    location = location.split('/')

    p_loc = parser.str_list_to_float_list(p_loc)
    location = parser.str_list_to_float_list(location)

    result = [abs(p_loc[0] - location[0]), abs(p_loc[1] - location[1])]

    return result


# 미세먼지, 초미세먼지 비교 (환자가 외출 시에만 비교함)
def dust_com(data):
    if (3 <= int(data['Finedust'])) or (3 <= int(data['UltraFinedust'])):
        return '미세먼지 혹은 초미세먼지 수치가 높습니다. 실내활동을 권장합니다.'
    return None


# 강수량 비교 (환자가 외출 시에만 비교함)
def pre_com(data):
    if data['Precipitation'] == '1':
        return '비가 오고 있습니다. 실내활동을 권장합니다.'
    elif data['Precipitation'] == '2':
        return '진눈깨비가 오고 있습니다. 실내활동을 권장합니다.'
    elif data['Precipitation'] == '3':
        return '눈이 오고 있습니다. 실내활동을 권장합니다.'
    elif data['Precipitation'] == '4':
        return '소나기가 오고 있습니다. 실내활동을 권장합니다.'
    return None


# 날씨 비교 (환자가 외출 시에만 비교함)
def sky_com(data):
    if data['Sky'] == '3':
        return '구름이 많습니다. 실내활동을 권장합니다.'
    elif data['Sky'] == '4':
        return '날씨가 흐립니다. 실내활동을 권장합니다.'
    return None


# 기온 비교 (환자가 외출 시에만 비교함)
def temp_com(data):
    if float(data['Temperatures']) < 10:
        return '기온이 ' + data['Temperatures'] + '도 입니다. 날씨가 추우므로 실내활동을 권장합니다.'
    elif 36 < float(data['Temperatures']):
        return '기온이 ' + data['Temperatures'] + '도 입니다. 날씨가 더우므로 실내활동을 권장합니다.'
    return None


# 조도 평균을 가져와서 수신받은 로그와 비교
# 시간에 따른 평균을 각각 구해야 할 것 같다.......
def illu_com(data):
    illu = int(data['Illuminance'])
    illu_avg_list = dao.get_today_avg(data['PatientSeq'])

    for illu_avg in illu_avg_list:
        illu_diff = illu - illu_avg[0]
        if illu_diff < -10:
            return '어제보다 조도가 ' + str(abs(illu_diff)) + '만큼 낮습니다.'
        elif 10 < illu_diff:
            return '어제보다 조도가 ' + str(abs(illu_diff)) + '만큼 높습니다.'
    return None


# 소음 평균을 가져와서 수신받은 로그와 비교
# 시간에 따른 평균을 각각 구해야 할 것 같다.......
def noise_com(data):
    noise = int(data['Noise'])
    noise_avg_list = dao.get_today_avg(data['PatientSeq'])

    for noise_avg in noise_avg_list:
        noise_diff = noise - noise_avg[1]
        if noise_diff < -10:
            return '어제보다 소음이 ' + str(abs(noise_diff)) + '만큼 낮습니다.'
        elif 10 < noise_diff:
            return '어제보다 소음이 ' + str(abs(noise_diff)) + '만큼 높습니다.'
    return None


# 금일 조도, 소음 평균값 DB 저장
# 시간에 따른 평균을 각각 구해야 할 것 같다.......
def insert_data_avg(data):
    # Delete all data int today_avg table.
    dao.del_all_data_today_avg()
    # 시간 값 추출 후 아침, 점심, 저녁, 밤으로 구분
    outdoor_data = dao.get_outdoor_data(data['PatientSeq'])
    day_time_data = [[], [], [], []]
    for val in outdoor_data:
        if 5 < val[2].time().hour < 12:
            day_time_data[0].append(val)
        elif 11 < val[2].time().hour < 18:
            day_time_data[1].append(val)
        elif 17 < val[2].time().hour < 22:
            day_time_data[2].append(val)
        elif (21 < val[2].time().hour) or (val[2].time().hour < 6):
            day_time_data[3].append(val)

    # day = [('95', '76', datetime.datetime(2019, 11, 5, 6, 30, 33)), ('95', '76', datetime.datetime......)]
    # val = ('95', '76', datetime.datetime(2019, 11, 5, 6, 30, 33)
    # 아침, 점심, 저녁, 밤 데이터를 평균을 구한 후, insert to today_avg.
    for i, day in enumerate(day_time_data):
        avg_list = [0, 0]
        val_cnt = 0
        for val in day:
            avg_list[0] += int(val[0])
            avg_list[1] += int(val[1])
            val_cnt += 1
        avg_list[0] = avg_list[0] / val_cnt
        avg_list[1] = avg_list[1] / val_cnt
        day_time_data[i] = avg_list

        day_time = 'MORNING'
        if i == 1:
            day_time = 'LUNCH'
        elif i == 2:
            day_time = 'DINNER'
        elif i == 3:
            day_time = 'NIGHT'
        dao.set_today_avg(data['PatientSeq'], day_time, avg_list[0], avg_list[1])


# 1. 환자가 외출 상태일 때, 외부 센서의 데이터를 통하여 날씨등의 위험요소 판단 후 result 변수에 append
# 2. 전일 조도, 소음의 평균값을 조회하여 금일과 비교 후 result 변수에 merge 후 데이터 송신
# (미세먼지/초미세먼지, 강수량, 날씨, 기온)
def chk_all(data):
    location = get_location(data['PatientSeq'], data['Location'])
    location_range = FileIO().read_location_info()
    result = []
    if (location_range['x'] <= location[0]) or (location_range['y'] <= location[1]):
        result.append(dust_com(data))
        result.append(pre_com(data))
        result.append(sky_com(data))
        result.append(temp_com(data))
    else:
        result.append(illu_com(data))
        result.append(noise_com(data))

    for msg in result:
        if msg is not None:
            obj = parser.make_requestObj('OutdoorSensing', msg, data['LogTime'], data['PatientSeq'])
            # 완성되면 이 부분의 주석을 풀어서 HIL 서버로 request를 날려. print 부분은 지워버리고....
            # requestData().postData(obj)
            print('chk_outdoor의 obj : ', obj)
