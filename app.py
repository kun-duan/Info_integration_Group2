from flask import *
from config import db
import random
import time
import config
import os
import re
app = Flask(__name__)
import cv2
import base64
@app.route('/')
def hello_world():
    return "hello word!"

#发布寻亲登记的信息
@app.route('/post_issue', methods=['GET', 'POST'])
def post_issue():
    if request.method == 'GET':
        return render_template('post_issue.html')
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        img = f.read()
        print('img', type(img))
        title = request.form.get('title')
        lost_place = request.form.get('lost_place')
        number = request.form.get('number')
        comment = request.form.get('editorValue')

        try:
            cur = db.cursor()

            sql = "INSERT INTO trace (title,description,lost_place,phone_number,picture) VALUES  (%s,%s,%s,%s,%s);"
            args = (title, comment,lost_place,number,img)
            cur.execute(sql, args)
            db.commit()
            cur.close()
            return render_template('formula.html')
        except Exception as e:
            raise e


#寻亲消息界面显示
@app.route('/formula')
def formula():
    if request.method == 'GET':
        try:
            cur = db.cursor()
           # sql = "select Issue.Ino, Issue.email,UserInformation.nickname,issue_time,Issue.title,Comment.comment from Issue,UserInformation,Comment where Issue.email = UserInformation.email and Issue.Ino = Comment.Ino and Cno = '1' order by issue_time DESC "
            sql = "select id,title,picture,lost_place,description,phone_number,picture from trace "

            db.ping(reconnect=True)
            cur.execute(sql)
            issue_information = cur.fetchall()

            # for issue in issue_information:
            #   base64.b64decode(issue[5])
            # sql = "select picture from trace "
            # db.ping(reconnect=True)
            # cur.execute(sql)
            # image = cur.fetchall()
            # for ima in image:
            #
            #   fout = open('image.png', 'wb')
            #   fout.write(ima[0])
            #   fout.close()

#返回救助金的剩余数目
            sql = "select sum(inflow.money_amount)-sum(outflow.money_amount) from inflow,outflow "
            db.ping(reconnect=True)
            cur.execute(sql)
            amount = cur.fetchall()
            #print(amount.type)
            amount1=str(amount[0][0])+'元'
            cur.close()
            return render_template('formula.html',issue_information = issue_information,amount1=amount1)
        except Exception as e:
            raise e

#判断前端提交的文件格式是否为图片的类型
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.run()
