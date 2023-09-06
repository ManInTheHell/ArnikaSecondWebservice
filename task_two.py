import requests


def task_two():
    response = requests.put('http://127.0.0.1:5000/reset/params/a')
    a = response.json().get('a')
    response = requests.put('http://127.0.0.1:5000/reset/params/b')
    b = response.json().get('b')
    print('two', a, b)
