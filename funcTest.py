from lib import controller
from lib.learner import Learner

learner = Learner(414, 1, 0, 0, 0)
process = learner.getProcess()

# controller.insert_data_avg()
# controller.all_user_insert_today_schedule(process, learner)
controller.all_user_chk_past_schedule()