from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def run_scheduler(job, hour, minute):
    schedule = BackgroundScheduler()
    schedule.add_job(job, 'cron', hour=hour, minute=minute)
    schedule.start()
    print('Scheduler is Running --- scheduled a job :', job.__name__, ' at ', hour, ':', minute)


def run_scheduler_use_param(job, param, hour, minute):
    schedule = BackgroundScheduler()
    schedule.add_job(job, 'cron', param, hour=hour, minute=minute)
    schedule.start()
    print('Scheduler is Running --- scheduled a job :', job.__name__, ' at ', hour, ':', minute)


def run_interval_scheduler(job, hour):
    schedule = BackgroundScheduler()
    schedule.add_job(job, 'interval', hours=hour)
    schedule.start()
    print('Interval Scheduler is Running --- scheduled a job :', job.__name__, ' interval :', hour)
