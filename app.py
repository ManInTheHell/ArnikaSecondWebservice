from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from task_one import task_one
from task_two import task_two

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(task_one, 'cron', hour='9-23', second='*/5')
scheduler.add_job(task_two, 'interval', seconds=10)
# scheduler.add_job(task_one, 'cron', hour='9-17', minute='*/2')
# scheduler.add_job(task_two, 'interval', hours=2)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, port=5050)
