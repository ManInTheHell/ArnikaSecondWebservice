from app import db


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value_a = db.Column(db.Float, nullable=False)
    value_b = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
