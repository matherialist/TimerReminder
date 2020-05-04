import requests
from flask import Flask, request

app = Flask(__name__)

address = 'http://127.0.0.1:6000/reminder'

r = requests.post(url=address, json={"days": 0, "hours": 0, "minutes": 0, "seconds": 10})


@app.route('/', methods=['POST'])
def wait_answer():
    data = request.get_json()
    print(data)
    return {"message": 'OK'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000)
