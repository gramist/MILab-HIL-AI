import json

from flask import Flask, abort, request, render_template
from flask_paginate import Pagination, get_page_args

from lib import parser, controller
from lib.fileIO import FileIO
from lib.learner import Learner

app = Flask(__name__)

learner = Learner(414, 1, 0, 0, 0)
process = learner.getProcess()


# 센서 페이징 받아오기
def get_users(offset=0, per_page=10):
    users = controller.get_abnormal_list(37)
    return users[offset: offset + per_page]


# 외부환경 페이징 받아오기
def get_posts1(offset=0, per_page=10):
    posts1 = controller.get_outdoor_list(37)
    return posts1[offset: offset + per_page]


# 이상행동 페이징 받아오기
def get_posts2(offset=0, per_page=10):
    posts2 = controller.get_past_schedule(37)
    return posts2[offset: offset + per_page]


# 스케줄 페이징 받아오기
def get_posts3(offset=0, per_page=10):
    posts3 = controller.get_today_schedule(37)
    return posts3[offset: offset + per_page]


@app.route('/<patient_seq>')
def main(patient_seq):
    index = controller.get_abnormal_week(patient_seq)
    return render_template("Hil_index.html", index=index)


# 이상증상 상세사항
@app.route('/table1/<patient_seq>')
def table1(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    users = controller.get_abnormal_list(patient_seq)
    total = len(users)
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_table1.html', users=pagination_users, page=page, per_page=per_page,
                           pagination=pagination)


# 외부환경 상세사항
@app.route('/table2/<patient_seq>')
def table2(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    posts1 = controller.get_outdoor_list(patient_seq)
    total = len(posts1)
    pagination_posts1 = get_posts1(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_table2.html', posts1=pagination_posts1, page=page, per_page=per_page,
                           pagination=pagination)


# 스케줄 미 이행 상세사항
@app.route('/table3/<patient_seq>')
def table3(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    posts2 = controller.get_past_schedule(patient_seq)
    total = len(posts2)
    pagination_posts2 = get_posts2(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_table3.html', posts2=pagination_posts2, page=page, per_page=per_page,
                           pagination=pagination)


@app.route('/map/<patient_seq>')
def map(patient_seq):
    location_list = controller.get_today_locations(patient_seq)
    return render_template("Hil_map.html", location_list=location_list)


# 스케줄 상세사항
@app.route('/schedule/<patient_seq>')
def schedule(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    posts3 = controller.get_today_schedule(patient_seq)
    total = len(posts3)
    pagination_posts3 = get_posts3(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_schedule.html', posts3=pagination_posts3, page=page, per_page=per_page,
                           pagination=pagination)


@app.route('/foo', methods=['GET', 'POST'])
def foo():
    if not request.json:
        abort(400)

    result_msg = {'ResultMessage': 'OK'}

    # # log = [YYYY - MM - DD, HH: MM:SS, sensor# , hash#]
    # # result = ['2019-08-05', '07:55:13', 1, 1]
    result = parser.json_parser(request.json)
    if type(result) == str:
        controller.abnormal_checker(request, result, process, learner)
    elif type(result) == dict:
        controller.chk_all(result)

    return json.dumps(result_msg)


if __name__ == '__main__':
    server_info = FileIO().read_server_info()

    # timeSchedule.run_scheduler(controller.insert_data_avg, 16, 32)
    # 머신러닝 학습, 스케줄 create 스케줄러 걸어야 함.
    # timeSchedule.run_scheduler(학습_함수, 23, 00) 이건 테스트 종료하고 제일 나중에 만들자....
    # timeSchedule.run_scheduler(스케줄 create, 23, 00)

    app.run(host=server_info['IP'], port=server_info['Port'], threaded=False)
    # app.run(host=server_info['IP'], port=server_info['Port'], debug=True, use_reloader=False)

# curl -i -H "Content-Type: application/json" -X POST -d "{\"PacketType\": \"SensorLog\", \"PatientSeq\": 37,
# \"SensorIdk\": \"A2:22:44:55:22:11\", \"SensorCode\": 3, \"SensorCount\": 16, \"LogTime\": \"2019-08-25 1:16:30\"}"
# 127.0.0.1:5000/foo
