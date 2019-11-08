import json


def list_to_str(data):
    # data = ['2019-08-25', '1:16:30', 3, 16]
    result = ''

    for i, val in enumerate(data):
        if i == len(data) - 1:
            result += (str(val))
        else:
            result += (str(val) + ', ')

    return result


def str_to_list(data):
    # data = '2019-08-25, 1:16:30, 3, 16'
    result = data.split(',')

    result[2] = int(result[2])
    result[3] = int(result[3])

    return result


# SensorLog와 OutdoorLog 판단 후, 파싱
def json_parser(data):
    # data = {"PacketType": "SensorLog",
    #         "PatientSeq": 37,
    #         "SensorIdk": "A2:22:44:55:22:11",
    #         "SensorCode": 3,
    #         "SensorCount": 1,
    #         "LogTime": "2019-08-25 1:16:30"}
    result = "none"

    if data["PacketType"] == "SensorLog":
        result = str(data['LogTime']).split(' ')
        result.append(data['SensorCode'])
        result.append(data['SensorCount'])

        result[2] = int(result[2])
        result[3] = int(result[3])
        result = list_to_str(result)

    elif data["PacketType"] == "OutdoorLog":
        result = data

    else:
        raise TypeError('This JSON Object is not SensorLog or OutdoorLog.')

    return result


def tuple_to_list(data):
    result = []

    for val in data:
        tmp = str(val[0]).split(',')
        tmp[2] = int(tmp[2])
        tmp[3] = int(tmp[3])
        result.append(tmp)

    return result


def make_requestObj(packet_type, packet_content, time, patient_seq):
    result = {
        'PacketType': packet_type,
        'PacketContent': packet_content,
        'Time': time,
        'PatientSeq': patient_seq
    }
    result = json.dumps(result, ensure_ascii=False)

    return result


def auto_parser(data):
    result = type(data)

    if type(result) == list:
        result = list_to_str(result)
    elif type(result) == str:
        result = str_to_list(result)
    elif type(result) == tuple:
        result = tuple_to_list(result)
    elif type(result) == dict:
        result = json_parser(result)
    else:
        raise TypeError('This is not the type of data supported by this program.')

    return result


def str_list_to_float_list(data):
    for i, val in enumerate(data):
        data[i] = float(val)
    return data
