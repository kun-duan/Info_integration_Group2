import wkh
import json
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/wkh')
def wkh():
    return render_template("try02.html")


@app.route('/ajax', methods=['post', 'get'])
def send_ajax():
    data = json.loads(request.values.get('data'))
    print(data)
    username = data['username']
    password = data['password']
    print(username)
    print(password)
    return "46575"


if __name__ == '__main__':
    app.run(debug=True)
