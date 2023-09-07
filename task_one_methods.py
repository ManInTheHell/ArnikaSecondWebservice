import requests
import datetime
import pandas as pd
from data_models import *
from app import app, db


def task_one():
    a, b, fetch_time = call_data_web_service()
    new_values_id = insert_data_to_db(a, b, fetch_time)
    statistics_processes(new_values_id)


def call_data_web_service():
    response = requests.get('http://127.0.0.1:5000/params').json()
    a = response.get('a')
    b = response.get('b')
    print('call one', a, b, datetime.datetime.now())
    return a, b, datetime.datetime.now()


def insert_data_to_db(a, b, fetch_time):
    with app.app_context():
        new_value = Values(value_a=a, value_b=b, datetime=fetch_time, date=fetch_time.date(), time=fetch_time.time())
        db.session.add(new_value)
        db.session.commit()
        return new_value.id


def statistics_processes(new_values_id):
    raw_data_df = fetch_raw_data_from_db()
    correlation(raw_data_df, new_values_id)
    standard_deviation(raw_data_df, new_values_id)


def fetch_raw_data_from_db():
    with app.app_context():
        query = db.session.query(Values.value_a, Values.value_b)
        results = query.all()
        df = pd.DataFrame(results, columns=['Value_a', 'Value_b'])
        return df


def correlation(df, new_values_id):
    correlation_value = calculate_correlation(df)
    fill_correlation_table(correlation_value, new_values_id)


def calculate_correlation(df):
    correlation_matrix = df.corr()
    return correlation_matrix.loc['Value_a', 'Value_b']


def fill_correlation_table(value, new_values_id):
    with app.app_context():
        if str(value) != 'nan':
            new_correlation = Correlation(correlation=value, value_id=new_values_id)
        else:
            new_correlation = Correlation(correlation=None, value_id=new_values_id)
        db.session.add(new_correlation)
        db.session.commit()


def standard_deviation(df, new_values_id):
    standard_deviation_a, standard_deviation_b = calculate_standard_deviation(df)
    fill_standard_deviation_table(standard_deviation_a, standard_deviation_b, new_values_id)


def calculate_standard_deviation(df):
    standard_deviation_values = df.std(axis=0)
    standard_deviation_a = standard_deviation_values['Value_a']
    standard_deviation_b = standard_deviation_values['Value_b']
    return standard_deviation_a, standard_deviation_b


def fill_standard_deviation_table(value_a, value_b, new_values_id):
    with app.app_context():
        if str(value_a) != 'nan':
            new_standard_deviation = StandardDeviation(std_deviation_a=value_a, std_deviation_b=value_b,
                                                       value_id=new_values_id)
        else:
            new_standard_deviation = StandardDeviation(std_deviation_a=None, std_deviation_b=None,
                                                       value_id=new_values_id)
        db.session.add(new_standard_deviation)
        db.session.commit()
