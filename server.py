import json

from flask import Flask, abort, request

from dao import dao
from lib import parser
from lib.fileIO import FileIO
from lib.learner import Learner


app = Flask(__name__)

learner = Learner(414, 1, 0, 0, 0)
process = learner.getProcess()


@app.route('/foo', methods=['GET', 'POST'])
def foo():
    if not request.json:
        abort(400)

    # # log = [YYYY - MM - DD, HH: MM:SS, sensor# , hash#]
    # # result = ['2019-08-05', '07:55:13', 1, 1]
    result = parser.json_parser(request.json)
    if type(result) == str:
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

            # 추후 이 아래에 DB insert, 알림 프로세스 제작 필요.
            print('status : ', status)
            result = {
                'ResultMessage': status
            }
            return json.dumps(result)

    # elif type(result) == dict:
    #     # 습도, 온도 Table과 비교. 미세먼지, 초미세먼지 상태 보고 나쁘면 DB insert, 알림 프로세스 제작 필요.

    result_msg = {
        'ResultMessage': 'OK'
    }

    return json.dumps(result_msg)


if __name__ == '__main__':
    server_info = FileIO().read_server_info()
    app.run(host=server_info['IP'], port=server_info['Port'], threaded=False)
    # app.run(host=server_info['IP'], port=server_info['Port'], debug=True, use_reloader=False)

# curl -i -H "Content-Type: application/json" -X POST -d "{\"PacketType\": \"SensorLog\", \"PatientSeq\": 37,
# \"SensorIdk\": \"A2:22:44:55:22:11\", \"SensorCode\": 3, \"SensorCount\": 16, \"LogTime\": \"2019-08-25 1:16:30\"}"
# 127.0.0.1:5000/foo
