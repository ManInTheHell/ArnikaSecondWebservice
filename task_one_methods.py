import requests
import datetime
from data_models import Values, db
from app import app


def task_one():
    a, b, fetch_time = call_data_web_service()
    insert_data_to_db(a, b, fetch_time)


def call_data_web_service():
    response = requests.get('http://127.0.0.1:5000/params').json()
    a = response.get('a')
    b = response.get('b')
    print('call one', a, b, datetime.datetime.now())
    return a, b, datetime.datetime.now()


def insert_data_to_db(a, b, fetch_time):
    pass
    with app.app_context():
        new_values = Values(value_a=a, value_b=b, datetime=fetch_time, date=fetch_time.date(), time=fetch_time.time())
        db.session.add(new_values)
        db.session.commit()
