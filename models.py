from views import db


class Esp(db.Model):
    __tablename__ = 'sensor_data'

    data_id = db.Column(db.Integer, primary_key = True)
    sensor = db.Column(db.String, nullable = False)
    sensor_value = db.Column(db.Float, nullable = False)
    date = db.Column(db.String, nullable = False)
    
    def __init__(self, data_id, sensor, sensor_value, date):
        self.data_id = data_id
        self.sensor = sensor
        self.sensor_value = sensor_value
        self.date = date

    def __repr__(self):
        return '<sensor {0}>'.format(self.sensor)
