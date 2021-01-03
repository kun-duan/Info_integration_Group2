from flask import Flask, render_template, request, json, jsonify
import data_query
import data_integrate
import wkh
import json

app = Flask(__name__)

'''
这一部分是段骞轶的功能，儿童信息登记查询
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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
    # 调用登记函数
    data_integrate.execute_insert(id_num)
    words = {'word': '导入、登记成功'}
    return words


@app.route('/inquiry/get_id', methods=['GET', 'POST'])
def query_get_id():
    key_value = request.values.get("key_value")
    res_t = data_query.data_query(key_value)
    res = json.dumps(res_t)
    print(type(res))
    return res


'''
这一部分是吴科慧的，主要用来显示管理员和普通用户的界面，以及发送ajax请求
'''


@app.route('/user', methods=['post', 'get'])
def user():
    return render_template("user.html")


@app.route('/ajax_user_submit', methods=['post', 'get'])
def ajax_user_submit():
    data1 = json.loads(request.values.get('data1'))
    p_id = data1['p_id']
    p_phone_number = data1['p_phone_number']
    p_audit_status = "成功提交"
    wkh.user_apply(p_id, p_phone_number, p_audit_status)
    filter_user = wkh.user_filter(p_id)
    if filter_user:
        wkh.update_status(p_id)
        pro = jsonify({"pro": "不符合申请要求"})
        return pro
    else:
        pro = jsonify({"pro": "申请提交成功"})
        return pro


@app.route('/ajax_user_search', methods=['post', 'get'])
def ajax_user_search():
    data2 = json.loads(request.values.get('data2'))
    query = data2['query']
    search_result = wkh.user_search(query)
    if search_result != 0:
        for i, data in enumerate(search_result):
            if data is None or data == "":
                search_result[i] = "暂无信息"
        json_result = jsonify({
            "name": search_result[0],
            "gender": search_result[1],
            "nation": search_result[2],
            "status": search_result[3]
        })
        return json_result
    else:
        json_result = jsonify({
            "p_id": "0"
        })
        return json_result


@app.route('/governor', methods=['post', 'get'])
def governor():
    return render_template("governor.html")


@app.route('/ajax_governor_submit', methods=['post', 'get'])
def ajax_governor_submit():
    data1 = json.loads(request.values.get('data1'))
    p_id = data1['p_id']
    c_id = data1['c_id']
    status = data1['status']
    # print(p_id, c_id, status)
    wkh.governor_register(p_id, c_id, status)
    pro = jsonify({"pro": "提交成功"})
    return pro


@app.route('/ajax_governor_search', methods=['post', 'get'])
def ajax_governor_search():
    data2 = json.loads(request.values.get('data2'))
    query = data2['query']
    search_result = wkh.governor_search(query)
    if search_result != 0:
        date_format = search_result[3].split("/")
        date_str = date_format[0] + "年" + date_format[1] + "月" + date_format[2] + "日"
        for i, data in enumerate(search_result):
            if data is None or data == "":
                search_result[i] = "暂无信息"
        json_result = jsonify({
            "p_id": search_result[0],
            "name": search_result[1],
            "gender": search_result[2],
            "date": date_str,
            "nation": search_result[4],
            "education_degree": search_result[5],
            "children": search_result[6],
            "crime": search_result[7],
            "current_province": search_result[8],
            "current_city": search_result[9],
            "credit_level": search_result[10],
            "fortune": search_result[11],
            "health_level": search_result[12],
            "audit_status": search_result[13],
            "phone_number": search_result[14],
            "adopted_children_id": search_result[15],
        })
        return json_result
    else:
        json_result = jsonify({
            "p_id": "0"
        })
        return json_result


if __name__ == '__main__':
    app.run(debug=True)
