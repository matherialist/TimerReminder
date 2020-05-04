from os import path
from flask import Flask, request
from TimerReminder import TimerReminder

app = Flask(__name__)

config_relative_path = 'files'
config_path = path.join(path.dirname(__file__), config_relative_path)

tr = TimerReminder()


@app.route('/reminder', methods=['POST'])
def reminder():
    data = request.get_json()
    address = 'http://' + request.remote_addr + ':7000'
    dt = tr.convert_to_datetime(data, diff=True)
    tr.add_reminder(dt, address)
    return {"message": 'OK'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
