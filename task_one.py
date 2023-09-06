import requests


def task_one():
    response = requests.get('http://127.0.0.1:5000/params').json()
    a = response.get('a')
    b = response.get('b')
    print('one', a, b)
