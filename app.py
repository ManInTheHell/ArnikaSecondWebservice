from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arnikadatabase.db'
db = SQLAlchemy(app)

from data_models import *
with app.app_context():
    db.create_all()

scheduler = BackgroundScheduler()
from task_one_methods import task_one
from task_two_methods import task_two
# scheduler.add_job(task_one, 'cron', hour='0-23', second='*/5')
# scheduler.add_job(task_two, 'interval', seconds=30)
scheduler.add_job(task_one, 'cron', hour='9-17', minute='*/2')
scheduler.add_job(task_two, 'interval', hours=2)
scheduler.start()


from end_points import *

if __name__ == '__main__':
    app.run(debug=True, port=5050)
