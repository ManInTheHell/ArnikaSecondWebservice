from app import db


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value_a = db.Column(db.Float, nullable=False)
    value_b = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)


class Correlation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correlation = db.Column(db.Float, nullable=False)
    value_id = db.Column(db.Integer, db.ForeignKey('values.id'))
    value = db.relationship('Values', backref='correlation')


class StandardDeviation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    std_deviation_a = db.Column(db.Float, nullable=False)
    std_deviation_b = db.Column(db.Float, nullable=False)
    value_id = db.Column(db.Integer, db.ForeignKey('values.id'))
    value = db.relationship('Values', backref='std_deviation')
