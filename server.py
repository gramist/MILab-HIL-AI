import json

from flask import Flask, abort, request, render_template

from dao import dao
from lib import parser
from lib import compare
from lib.fileIO import FileIO
from lib.learner import Learner
from lib.requestData import requestData

app = Flask(__name__)

learner = Learner(414, 1, 0, 0, 0)
process = learner.getProcess()

#post는 index값, symp값, time값을 인자로 받습니다.
posts=[
    { 'index':'10','symp':'불면','time':'2019-01-02 / 22:08:30'},
    { 'index':'9','symp':'공격적인 행동','time':'2019-01-02 / 22:08:30'}
]

#post1~3까지는 time값과 name값을 인자로 받습니다.
posts1=[
    { 'time':'2019-01-02 / 21:08:30','name':'초미세먼지 나쁨 / 3 / 실내활동을 권장합니다'},
    { 'time':'2019-01-02 / 21:08:30','name':'미세먼지 매우나쁨 / 4 / 실내활동을 권장합니다'}
]

posts2=[
    { 'time':'2019-01-02 / 21:08:30','name':'약을 복용하지 않았습니다.'},
    { 'time':'2019-01-02 / 21:08:30','name':'약을 복용하지 않았습니다.'}
]

posts3=[
    { 'time':'2019-01-02 / 07:00-08:00','name':'기상'},
    { 'time':'2019-01-02 / 07:00-08:00','name':'기상'}
]

#index는 퍼센트만 받아오면 됩니다. 혹은 행동을 한 횟수로 가져와도 됩니다.=>행동으로 받아올경우 %가아닌 px단위로 가져오기 때문에 그래프가 이상합니다.
#한마디로 행동 횟수는 10회라고 가정하면 10%로 가져오는게 좋습니다.
index=[
    { 'name':'배회','per':'30%'},
    { 'name':'낙상','per':'50%'},
    { 'name':'수집','per':'60%'},
    { 'name':'과식','per':'45%'},
    { 'name':'부적절한 성적행동','per':'32%'},
    { 'name':'망상','per':'62%'},
    { 'name':'공격적인 행동','per':'75%'}
]

@app.route('/')
def main():
    return render_template("Hil_index.html")


@app.route('/table1')
def table1():
    return render_template("Hil_table1.html")


@app.route('/table2')
def table2():
    return render_template("Hil_table2.html")


@app.route('/table3')
def table3():
    return render_template("Hil_table3.html")


@app.route('/map')
def map():
    location_list = controller.get_today_locations(40)
    # print(location_list)
    return render_template("Hil_map.html", location_list=location_list)


@app.route('/schedule')
def schedule():
    return render_template("Hil_schedule.html")


@app.route('/foo', methods=['GET', 'POST'])
def foo():
    if not request.json:
        abort(400)

    result_msg = {
        'ResultMessage': 'OK'
    }

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
            if status is not None:
                obj = parser.make_requestObj(
                    'AbnormalBehavior',
                    status,
                    request.json['LogTime'],
                    request.json['PatientSeq']
                )
                requestData().postData(obj)

            return json.dumps(result_msg)

    elif type(result) == dict:
        controller.chk_all(result)

    return json.dumps(result_msg)


if __name__ == '__main__':
    server_info = FileIO().read_server_info()

    timeSchedule.run_scheduler(controller.insert_data_avg, 16, 32)
    # 머신러닝 학습, 스케줄 create 스케줄러 걸어야 함.
    # timeSchedule.run_scheduler(학습_함수, 23, 00)\
    # timeSchedule.run_scheduler(스케줄 create, 23, 00)

    app.run(host=server_info['IP'], port=server_info['Port'], threaded=False)
    # app.run(host=server_info['IP'], port=server_info['Port'], debug=True, use_reloader=False)

# curl -i -H "Content-Type: application/json" -X POST -d "{\"PacketType\": \"SensorLog\", \"PatientSeq\": 37,
# \"SensorIdk\": \"A2:22:44:55:22:11\", \"SensorCode\": 3, \"SensorCount\": 16, \"LogTime\": \"2019-08-25 1:16:30\"}"
# 127.0.0.1:5000/foo
