# learner = Learner(414, 1, 0, 0, 0)
# process = learner.getProcess()
#
# # controller.insert_data_avg()
# # controller.all_user_insert_today_schedule(process, learner)
# controller.all_user_chk_past_schedule()
# from lib import controller
#
# a = controller.get_sensor_list(80)
# print(a)
#
# from dao import dao
#
# outdoor_recent_date = dao.get_outdoor_logtime()
# outdoor_recent_date = outdoor_recent_date[0][0].split(' ')[0]
# print(dao.get_outdoor_data(outdoor_recent_date))
from dao import dao
from lib import controller, learner, processData

# controller.insert_data_avg()
# from lib.controller import set_ai_schedule_data
#
# set_ai_schedule_data()
get_data = controller.get_sensor_list(108)
cnt_list = controller.get_sensor_cnt_list(get_data)
#
# print(get_data)
# print(cnt_list)
# from lib.learner import Learner
#
# learner = Learner(414, 1, 0, 0, 0)
# process = learner.getProcess()
#
# batch = process.process(108)
# schedule_data = learner.make_schedule(batch)