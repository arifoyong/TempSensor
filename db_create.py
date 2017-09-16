from views import db
from models import Esp
import time

#Create the database
db.create_all()

#insert initial data
now = time.localtime()
data_id = int(time.mktime(now))
date = time.strftime('%Y-%m-%d %H:%M:%S', now)
data = {'data_id': data_id, 'sensorType': 'Temperature', 'values': [21.2], 'date':date}
db.session.add(Esp(data['data_id'], data['sensorType'], data['values'][0], data['date']))

#Commit changes
db.session.commit()
