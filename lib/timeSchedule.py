from apscheduler.schedulers.background import BackgroundScheduler


def run_scheduler(job, hour, minute):
    schedule = BackgroundScheduler()
    schedule.add_job(job, 'cron', hour=hour, minute=minute)
    schedule.start()
    print('Scheduler is Running --- scheduled a job :', job.__name__, ' at ', hour, ':', minute)
