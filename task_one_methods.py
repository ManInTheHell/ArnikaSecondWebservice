import requests
import datetime
from pandas import DataFrame
from data_models import *
from app import app, db


def task_one():
    a, b, fetch_time = call_data_web_service()
    new_values_id_and_datetime = insert_data_to_db(a, b, fetch_time)
    statistics_processes(new_values_id_and_datetime)


def call_data_web_service():
    response = requests.get('http://127.0.0.1:5000/params').json()
    a = response.get('a')
    b = response.get('b')
    print('call one', a, b, datetime.datetime.now())
    return a, b, datetime.datetime.now()


def insert_data_to_db(a, b, fetch_time):
    with app.app_context():
        new_value = Values(value_a=a, value_b=b, datetime=fetch_time)
        db.session.add(new_value)
        db.session.commit()
        return new_value.id, new_value.datetime


def statistics_processes(new_values_id_and_datetime):
    raw_data_df = fetch_raw_data_from_db()
    correlation(raw_data_df, new_values_id_and_datetime)
    standard_deviation(raw_data_df, new_values_id_and_datetime)
    max_min_diff(raw_data_df)


def fetch_raw_data_from_db():
    with app.app_context():
        results = db.session.query(Values.id, Values.value_a, Values.value_b, Values.datetime).all()
        df = DataFrame(results, columns=['id', 'Value_a', 'Value_b', 'datetime'])
        return df


def correlation(df, new_values_id_and_datetime):
    correlation_value = calculate_correlation(df)
    fill_correlation_table(correlation_value, new_values_id_and_datetime)


def calculate_correlation(df):
    just_values_df = df.copy()
    just_values_df.drop(columns=['id', 'datetime'], inplace=True)
    correlation_matrix = just_values_df.corr()
    return correlation_matrix.loc['Value_a', 'Value_b']


def fill_correlation_table(value, new_values_id_and_datetime):
    with app.app_context():
        if str(value) != 'nan':
            new_correlation = Correlation(correlation=value, value_id=new_values_id_and_datetime[0],
                                          datetime=new_values_id_and_datetime[1])
        else:
            new_correlation = Correlation(correlation=None, value_id=new_values_id_and_datetime[0],
                                          datetime=new_values_id_and_datetime[1])
        db.session.add(new_correlation)
        db.session.commit()


def standard_deviation(df, new_values_id_and_datetime):
    standard_deviations = calculate_standard_deviation(df)
    fill_standard_deviation_table(standard_deviations, new_values_id_and_datetime)


def calculate_standard_deviation(df):
    just_values_df = df.copy()
    just_values_df.drop(columns=['id', 'datetime'], inplace=True)
    standard_deviation_values = just_values_df.std(axis=0)
    standard_deviation_a = standard_deviation_values['Value_a']
    standard_deviation_b = standard_deviation_values['Value_b']
    return standard_deviation_a, standard_deviation_b


def fill_standard_deviation_table(args, new_values_id_and_datetime):
    with app.app_context():
        if str(args[0]) != 'nan':
            new_standard_deviation = StandardDeviation(std_deviation_a=args[0], std_deviation_b=args[1],
                                                       value_id=new_values_id_and_datetime[0],
                                                       datetime=new_values_id_and_datetime[1])
        else:
            new_standard_deviation = StandardDeviation(std_deviation_a=None, std_deviation_b=None,
                                                       value_id=new_values_id_and_datetime[0],
                                                       datetime=new_values_id_and_datetime[1])
        db.session.add(new_standard_deviation)
        db.session.commit()


def max_min_diff(df):
    if len(df) > 1:
        max_min_diff_tuple_values = calculate_max_min_diff(df)
        fill_max_min_diff_tables(max_min_diff_tuple_values)


def calculate_max_min_diff(df):
    copy_df = df.copy()
    copy_df = copy_df.sort_values(by='datetime')
    copy_df['delta_a'] = copy_df['Value_a'].diff()
    copy_df['delta_b'] = copy_df['Value_b'].diff()

    max_diff_a = copy_df.loc[copy_df['delta_a'].idxmax()]
    min_diff_a = copy_df.loc[copy_df['delta_a'].idxmin()]
    max_diff_b = copy_df.loc[copy_df['delta_b'].idxmax()]
    min_diff_b = copy_df.loc[copy_df['delta_b'].idxmin()]
    return max_diff_a, min_diff_a, max_diff_b, min_diff_b


def fill_max_min_diff_tables(args):
    last_records = fetch_last_records_value_id()
    if last_records[0] != args[0]['id']:
        with app.app_context():
            new_max_diff_a = MaxDiffA(max_diff_a=args[0]['delta_a'], datetime=args[0]['datetime'],
                                      value_id=int(args[0]['id']))
            db.session.add(new_max_diff_a)
            db.session.commit()

    if last_records[1] != args[1]['id']:
        with app.app_context():
            new_min_diff_a = MinDiffA(min_diff_a=args[1]['delta_a'], datetime=args[1]['datetime'],
                                      value_id=int(args[1]['id']))
            db.session.add(new_min_diff_a)
            db.session.commit()

    if last_records[2] != args[2]['id']:
        with app.app_context():
            new_max_diff_b = MaxDiffB(max_diff_b=args[2]['delta_b'], datetime=args[2]['datetime'],
                                      value_id=int(args[2]['id']))
            db.session.add(new_max_diff_b)
            db.session.commit()

    if last_records[3] != args[3]['id']:
        with app.app_context():
            new_min_diff_b = MinDiffB(min_diff_b=args[3]['delta_b'], datetime=args[3]['datetime'],
                                      value_id=int(args[3]['id']))
            db.session.add(new_min_diff_b)
            db.session.commit()


def fetch_last_records_value_id():
    with app.app_context():
        latest_record_max_diff_a = db.session.query(MaxDiffA).order_by(MaxDiffA.datetime.desc()).first()
        latest_record_min_diff_a = db.session.query(MinDiffA).order_by(MinDiffA.datetime.desc()).first()
        latest_record_max_diff_b = db.session.query(MaxDiffB).order_by(MaxDiffB.datetime.desc()).first()
        latest_record_min_diff_b = db.session.query(MinDiffB).order_by(MinDiffB.datetime.desc()).first()
        if latest_record_max_diff_a is None:
            latest_record_max_diff_a = 0
        else:
            latest_record_max_diff_a = latest_record_max_diff_a.value_id
        if latest_record_min_diff_a is None:
            latest_record_min_diff_a = 0
        else:
            latest_record_min_diff_a = latest_record_min_diff_a.value_id
        if latest_record_max_diff_b is None:
            latest_record_max_diff_b = 0
        else:
            latest_record_max_diff_b = latest_record_max_diff_b.value_id
        if latest_record_min_diff_b is None:
            latest_record_min_diff_b = 0
        else:
            latest_record_min_diff_b = latest_record_min_diff_b.value_id

    return latest_record_max_diff_a, latest_record_min_diff_a, latest_record_max_diff_b, latest_record_min_diff_b
