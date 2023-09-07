from flask import jsonify
from pandas import DataFrame

from app import app, db
from data_models import *


@app.route('/last/params', methods=['GET'])
def get_last_parameters():
    last_params = db.session.query(Values).order_by(Values.datetime.desc()).first()

    response_data = {
        'id': last_params.id,
        'last_value_a': last_params.value_a,
        'last_value_b': last_params.value_b,
        'datetime': last_params.datetime
    }

    return jsonify(response_data)


@app.route('/history/params', methods=['GET'])
def get_history_parameters():
    history_params = db.session.query(Values).all()
    response_data_list = []
    for param in history_params:
        response_data_list.append({
            'id': param.id,
            'last_value_a': param.value_a,
            'last_value_b': param.value_b,
            'datetime': param.datetime
        })

    return jsonify(response_data_list)


@app.route('/history/params/<string:parameter>', methods=['GET'])
def get_history_of_one_parameter(parameter):
    history_params = db.session.query(Values).all()
    response_data_list = []
    if parameter == 'a':
        for param in history_params:
            response_data_list.append({
                'id': param.id,
                'last_value_a': param.value_a,
                'datetime': param.datetime
            })
    elif parameter == 'b':
        for param in history_params:
            response_data_list.append({
                'id': param.id,
                'last_value_b': param.value_b,
                'datetime': param.datetime
            })
    else:
        return jsonify({'message': 'Not valid!'})

    return jsonify(response_data_list)


@app.route('/history/ratio', methods=['GET'])
def get_ratio_of_parameters():
    history_params = db.session.query(Values).all()
    response_data_list = []
    for param in history_params:
        response_data_list.append({
            'id': param.id,
            'ratio': param.value_a / param.value_b,
            'datetime': param.datetime
        })

    return jsonify(response_data_list)


@app.route('/last/statistics', methods=['GET'])
def get_last_statistics():
    last_correlation = db.session.query(Correlation).order_by(Correlation.value_id.desc()).first()
    last_standard_deviation = db.session.query(StandardDeviation).order_by(StandardDeviation.value_id.desc()).first()
    last_max_diff_a = db.session.query(MaxDiffA).order_by(MaxDiffA.datetime.desc()).first()
    last_min_diff_a = db.session.query(MinDiffA).order_by(MinDiffA.datetime.desc()).first()
    last_max_diff_b = db.session.query(MaxDiffB).order_by(MaxDiffB.datetime.desc()).first()
    last_min_diff_b = db.session.query(MinDiffB).order_by(MinDiffB.datetime.desc()).first()

    response_data_list = [{'id': last_correlation.id,
                           'value_id': last_correlation.value_id,
                           'correlation': last_correlation.correlation,
                           'datetime': last_correlation.datetime
                           },
                          {
                              'id': last_standard_deviation.id,
                              'value_id': last_standard_deviation.value_id,
                              'std_deviation_a': last_standard_deviation.std_deviation_a,
                              'std_deviation_b': last_standard_deviation.std_deviation_b,
                              'datetime': last_standard_deviation.datetime
                          },
                          {
                              'id': last_max_diff_a.id,
                              'value_id': last_max_diff_a.value_id,
                              'max_diff_a': last_max_diff_a.max_diff_a,
                              'datetime': last_max_diff_a.datetime
                          },
                          {
                              'id': last_min_diff_a.id,
                              'value_id': last_min_diff_a.value_id,
                              'min_diff_a': last_min_diff_a.min_diff_a,
                              'datetime': last_min_diff_a.datetime
                          },
                          {
                              'id': last_max_diff_b.id,
                              'value_id': last_max_diff_b.value_id,
                              'max_diff_b': last_max_diff_b.max_diff_b,
                              'datetime': last_max_diff_b.datetime
                          },
                          {
                              'id': last_min_diff_b.id,
                              'value_id': last_min_diff_b.value_id,
                              'min_diff_b': last_min_diff_b.min_diff_b,
                              'datetime': last_min_diff_b.datetime
                          }
                          ]

    return jsonify(response_data_list)


@app.route('/history/statistics', methods=['GET'])
def get_ratio_of_parametere():
    history_correlation = db.session.query(Correlation).all()
    history_standard_deviation = db.session.query(StandardDeviation).all()
    history_max_diff_a = db.session.query(MaxDiffA).all()
    history_min_diff_a = db.session.query(MinDiffA).all()
    history_max_diff_b = db.session.query(MaxDiffB).all()
    history_min_diff_b = db.session.query(MinDiffB).all()

    history_correlation_data_list = []
    history_standard_deviation_data_list = []
    history_max_diff_a_data_list = []
    history_min_diff_a_data_list = []
    history_max_diff_b_data_list = []
    history_min_diff_b_data_list = []
    for record in history_correlation:
        history_correlation_data_list.append({'id': record.id, 'value_id': record.value_id,
                                              'correlation': record.correlation, 'datetime': record.datetime})
    for record in history_standard_deviation:
        history_standard_deviation_data_list.append({'id': record.id, 'value_id': record.value_id,
                                                     'std_deviation_a': record.std_deviation_a,
                                                     'std_deviation_b': record.std_deviation_a,
                                                     'datetime': record.datetime})
    for record in history_max_diff_a:
        history_max_diff_a_data_list.append({'id': record.id, 'value_id': record.value_id,
                                             'max_diff_a': record.max_diff_a, 'datetime': record.datetime})
    for record in history_min_diff_a:
        history_min_diff_a_data_list.append({'id': record.id, 'value_id': record.value_id,
                                             'min_diff_a': record.min_diff_a, 'datetime': record.datetime})
    for record in history_max_diff_b:
        history_max_diff_b_data_list.append({'id': record.id, 'value_id': record.value_id,
                                             'max_diff_b': record.max_diff_b, 'datetime': record.datetime})
    for record in history_min_diff_b:
        history_min_diff_b_data_list.append({'id': record.id, 'value_id': record.value_id,
                                             'min_diff_b': record.min_diff_b, 'datetime': record.datetime})

    response_data_list = [history_correlation_data_list, history_standard_deviation_data_list,
                          history_max_diff_a_data_list, history_min_diff_a_data_list,
                          history_max_diff_b_data_list, history_min_diff_b_data_list]

    return jsonify(response_data_list)


@app.route('/history/corr/std', methods=['GET'])
def get_corr_std_parameter():
    history_correlation = db.session.query(Correlation.correlation).all()
    df = DataFrame(history_correlation, columns=['correlation'])
    corr_std = df.std(axis=0)
    response_data = {'corr_std': corr_std.values[0]}
    return jsonify(response_data)
