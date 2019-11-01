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
    p_loc = dao.get_patient_location(patientSeq)
    p_loc = p_loc.split('/')
    location = location.split('/')

    result = [abs(p_loc[0] - location[0]), abs(p_loc[1] - location[1])]

    return result


# 환자가 외출 상태일 때, 외부 센서의 데이터를 통하여 날씨등의 위험요소 판단 후 데이터 송신
def chk_outdoor(data):
    location = get_location(data['PatientSeq'], data['Location'])
    location_range = FileIO().read_location_info()
    result = []
    if (location_range['x'] <= location[0]) or (location_range['y'] <= location[1]):
        result.append(dust_com(data))
        result.append(pre_com(data))
        result.append(sky_com(data))
        result.append(temp_com(data))

        for msg in result:
            if msg is not None:
                obj = parser.make_requestObj('OutdoorSensing', msg, data['LogTime'], data['PatientSeq'])
                requestData().postData(obj)


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
    if int(data['Temperatures']) < 10:
        return '기온이 ' + data['Temperatures'] + '도 입니다. 날씨가 추우므로 실내활동을 권장합니다.'
    elif 36 < int(data['Temperatures']):
        return '기온이 ' + data['Temperatures'] + '도 입니다. 날씨가 더우므로 실내활동을 권장합니다.'
    return None


# 조도 비교
def illu_com(data):
    illu = int(data['Illuminance'])
    illu_avg = int(dao.get_today_avg(data['PatientSeq'])[0])
    illu_diff = illu - illu_avg

    if illu_diff < -10:
        return '어제보다 조도가 ' + str(illu_diff) + '만큼 낮습니다.'
    elif 10 < illu_diff:
        return '어제보다 조도가 ' + str(illu_diff) + '만큼 높습니다.'
    return None


# 소음 비교
def noise_com(data):
    noise = int(data['Noise'])
    noise_avg = int(dao.get_today_avg(data['PatientSeq'])[1])
    noise_diff = noise - noise_avg

    if noise_diff < -10:
        return '어제보다 소음이 ' + str(noise_diff) + '만큼 낮습니다.'
    elif 10 < noise_diff:
        return '어제보다 소음이 ' + str(noise_diff) + '만큼 높습니다.'
    return None


# 금일 조도, 소음 평균값 DB 저장
def insert_data_avg(data, patient_seq):
    # (('95', '76'), ('95', '76'), ...)
    arr = [[], []]
    for tmp in data:
        arr[0].append(tmp[0])
        arr[1].append(tmp[1])
    i = 0
    j = 0
    for tmp_arr in arr:
        tmp_val = 0
        for val in tmp_arr:
            tmp_val += int(val)
            j += 1
        arr[i] = int(tmp_val / j)
        i += 1
        j = 0

        dao.set_today_avg(patient_seq, 0, arr[0], arr[1])
