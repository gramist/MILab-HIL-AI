import json
import os

from flask import Flask, abort, request, render_template
from flask_paginate import Pagination, get_page_args

from lib import parser, controller, timeSchedule
from lib.fileIO import FileIO
from lib.learner import Learner

app = Flask(__name__)
print(os.path.dirname(os.path.realpath(__file__)))
os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.getcwd())
learner = Learner(414, 1, 0, 0, 0)
process = learner.getProcess()


# 이상증세, 외부센서, 스케줄 미 이행, 머신러닝 스케줄 리스트를 참고한 페이징 get
def get_paging(data, offset=0, per_page=10):
    return data[offset: offset + per_page]


@app.route('/<patient_seq>')
def main(patient_seq):
    # get_row = 5
    index = controller.get_abnormal_week(patient_seq)
    return render_template("Hil_index.html", index=index)


# 이상증상 상세사항
@app.route('/table1/<patient_seq>')
def table1(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    users = controller.get_abnormal_list(patient_seq)
    total = len(users)
    pagination_users = get_paging(users, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_table1.html', users=pagination_users, page=page, per_page=per_page,
                           pagination=pagination)


# 외부환경 상세사항
@app.route('/table2/<patient_seq>')
def table2(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    posts1 = controller.get_outdoor_list(patient_seq)
    total = len(posts1)
    pagination_posts1 = get_paging(posts1, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_table2.html', posts1=pagination_posts1, page=page, per_page=per_page,
                           pagination=pagination)


# 스케줄 미 이행 상세사항
@app.route('/table3/<patient_seq>')
def table3(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    posts2 = controller.get_past_schedule(patient_seq)
    total = len(posts2)
    pagination_posts2 = get_paging(posts2, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_table3.html', posts2=pagination_posts2, page=page, per_page=per_page,
                           pagination=pagination)


@app.route('/map/<patient_seq>')
def patient_map(patient_seq):
    first_location = controller.get_patient_first_location(patient_seq)
    location_list = controller.get_today_locations(patient_seq)
    return render_template("Hil_map.html", first_location=first_location, location_list=location_list)


# 스케줄 상세사항
@app.route('/schedule/<patient_seq>')
def schedule(patient_seq):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    posts3 = controller.get_today_schedule(patient_seq)
    total = len(posts3)
    pagination_posts3 = get_paging(posts3, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Hil_schedule.html', posts3=pagination_posts3, page=page, per_page=per_page,
                           pagination=pagination)


# 가이드라인
@app.route('/guide/<patient_seq>')
def guide(patient_seq):
    g_opinion = controller.get_guide_opinion(patient_seq)
    p_health_info = controller.get_guide_scores(patient_seq)
    return render_template('Hil_guide.html', g_opinion=g_opinion, p_health_info=p_health_info, patient_seq=patient_seq)


# 신체상태, 청결상태, 낙상위험도, 인지기능 관찰, 욕창위험도 목록
@app.route('/<_type>/<patient_seq>')
def detailcon(_type, patient_seq):
    typetotxt = {'bodycon': '신체상태 관찰', 'cleancon': '청결상태', 'fallcon': '낙상 위험도', 'cognicon': '인지기능 관찰', 'decubcon': '욕창 위험도'}
    cond_info = controller.get_cond_info(patient_seq, _type)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(cond_info)
    pagination_infos = get_paging(cond_info, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Hil_detailcon.html', cond_infos=pagination_infos, title=typetotxt[_type], page=page, per_page=per_page,
                           pagination=pagination)


# 건강상태 목록
@app.route('/healthcon/<patient_seq>')
def healthcon(patient_seq):
    p_health_info = controller.get_health_info(patient_seq)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(p_health_info)
    pagination_infos = get_paging(p_health_info, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Hil_healthcon.html', health_infos=pagination_infos, page=page,
                           per_page=per_page,pagination=pagination)


# 최신 건강상태 상세(혈당, 혈압, 청취능력, 의사소통, 발음능력, 상처, 발생여부)
@app.route('/health_recent/<patient_seq>')
def health_recent(patient_seq):
    p_health_info = controller.get_health_info(patient_seq)[0]
    return render_template('Hil_health_recent.html', p_health_info=p_health_info)


@app.route('/ml/<patient_seq>')
def ml_page(patient_seq):
    acc_loss = controller.get_ml_val(patient_seq)
    return render_template('ml_page.html', acc_loss=acc_loss)


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

    # 외부 센서 평균 계산 후 table에 적재
    timeSchedule.run_scheduler(controller.insert_data_avg, 23, 00)
    # 모든 유저 오늘자 AI 스케줄 생성 후 table에 적재
    timeSchedule.run_scheduler_use_param(controller.all_user_insert_today_schedule, [process, learner], 23, 00)
    # 모든 유저들의 스케줄을 참조하여 하지 않은 일 알림
    timeSchedule.run_interval_scheduler(controller.all_user_chk_past_schedule, 1)

    app.run(host=server_info['IP'], port=server_info['Port'], threaded=False)
