from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import time
import json

async_mode = None
app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode=async_mode)

from models import Esp


def model_to_dict(model_instance):
    return {c.name: str(getattr(model_instance, c.name))
            for c in model_instance.__table__.columns}


def emit_data():
    query = db.session.query(Esp).order_by(Esp.data_id.desc()).limit(1).all()
    last_data = query[0].__dict__

    socketio.emit('my_response',
                  {'data_id': last_data['data_id'],
                   'sensor': last_data['sensor'],
                   'sensor_value': last_data['sensor_value'],
                   'date': last_data['date']},
                  namespace='/test')

    return "data emitted"


@app.route('/postjson', methods=['POST'])
def postJsonHandler():
    data = request.get_json()

    if db.session.query(Esp).count() > 100:
        query = db.session.query(Esp).order_by(Esp.data_id.desc()).limit(100)
        old_id = query[99].data_id

        db.session.query(Esp).filter(Esp.data_id < old_id).delete()
        db.session.commit()

    now = time.localtime()
    new_data = Esp(int(time.mktime(now)),
                   data['sensorType'],
                   data['values'][0],
                   time.strftime('%Y-%m-%d %H:%M:%S', now))
    db.session.add(new_data)
    db.session.commit()
    emitData = emit_data()
    return emitData


@app.route('/data')
def data():
    query = db.session.query(Esp).order_by(Esp.data_id.desc()).limit(10).all()
    dataToSend = [{"data_id": q.data_id,
                   "sensor": q.sensor,
                   "sensor_value": q.sensor_value,
                   "date": q.date
                   } for q in query]
    return json.dumps(dataToSend)


@socketio.on('connect', namespace='/test')
def connected():
    print("1st connection")
    emit_data()


@app.route('/')
def main():
    return render_template('main.html', async_mode=socketio.async_mode)

# query = db.session.query(Esp).order_by(Esp.data_id.desc()).limit(1).all()
# data = [{"data_id": q.data_id} for q in query]
