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


def json_to_str(data):
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
        # print('after parser : ', result)
    else:
        result = str(data["PatientSeq"]) + "," + data["Location"] + "," + data["LogTime"]
        result = list_to_str(result)

    return result

    # log shape shoud be [YYYY-MM-DD, HH:MM:SS, sensor#, hash#] (# is number)


def tuple_to_list(data):
    result = []

    for val in data:
        tmp = str(val[0]).split(',')
        tmp[2] = int(tmp[2])
        tmp[3] = int(tmp[3])
        result.append(tmp)

    return result
