from flask import Flask, render_template, request
# import data_integrate

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def user():
    return render_template('导航栏div部分.html')


@app.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    return render_template('children_inquiry.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('children_register.html')


@app.route('/register/get_id', methods=['GET', 'POST'])
def get_id():
    id_num = request.values.get("id_num")
    print(id_num)
    #调用登记函数
    # data_integrate.execute_insert(id_num)
    words = {'word': '成功接收'}
    return words


@app.route('/inquiry/get_id', methods=['GET', 'POST'])
def query():
    id_num = request.values.get("id_num")
    print(id_num)
    words = {'word': '成功接收'}
    return words


if __name__ == '__main__':
    app.run()
