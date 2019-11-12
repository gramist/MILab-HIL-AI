from dao import dao
from lib import parser


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
