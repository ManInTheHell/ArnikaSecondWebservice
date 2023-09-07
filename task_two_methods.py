import datetime

import requests


def task_two():
    print(f'start task two in: {datetime.datetime.now()}')
    response = requests.put('http://127.0.0.1:5000/reset/params/a')
    a = response.json().get('a')
    response = requests.put('http://127.0.0.1:5000/reset/params/b')
    b = response.json().get('b')
    print('reset values: ', a, b)
    print(f'end task two in: {datetime.datetime.now()}')
    print('---------------------------------------------------')
