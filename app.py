from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def user():
    return render_template('children_inquiry.html')


@app.route('/get_id', methods=['GET', 'POST'])
def get_id():
    id_num = request.values.get("id_num")
    print(id_num)
    words = {'word': '成功接收'}
    return words


if __name__ == '__main__':
    app.run()
