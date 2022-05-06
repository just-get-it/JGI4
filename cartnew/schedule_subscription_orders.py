# import schedule
# import time
from .views import checkSubOrders

# def job():
#     print("I'm working...")

# def schedule_task():
#     print("in task")
#     schedule.every(1).seconds.do(job)
#     # schedule.every().day.at("20:30").do(checkSubOrders)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print("Helloworld!")

def start():
    print("in start")
    scheduler = BackgroundScheduler()
    scheduler.add_job(checkSubOrders, 'cron', hour=22, minute=43, id="sub_order_001", replace_existing=True)
    scheduler.start()