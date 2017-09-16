from views import db
from _config import DATABASE_PATH

import sqlite3
import datetime

with sqlite3.connect(DATABASE_PATH) as con:
    c = con.cursor()

    c.execute('ALTER TABLE sensor_data RENAME TO old_sensor_data')

    db.create_all()

    c.execute('SELECT data_id, sensor, sensor_value FROM old_sensor_data ORDER BY data_id')
    data = [(row[0], row[1], row[2], datetime.datetime.utcnow()) for row in c.fetchall()]
    print(data)
    
    c.executemany('INSERT INTO sensor_data(data_id, sensor, sensor_value, date) VALUES(?,?,?,?)', data)
    
    

#Create the database
#db.create_all()

#insert initial data
#data = {'sensorType': 'Temperature', 'values': [20]}
#db.session.add(Esp(data['sensorType'], data['values'][0]))

#Commit changes
#db.session.commit()
