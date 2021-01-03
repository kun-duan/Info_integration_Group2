from flask import *
from flask import Flask, render_template
import json
from flask import jsonify
import pymysql
app = Flask(__name__)
app.secret_key='yxy'



@app.route('/')
def index():
    return render_template('fulizijin.html')


@app.route('/',methods=['POST'])
def method():
    # 资金流入登记
    #获取输入的姓名，身份证号码，金额以及时间
    don = request.form['don']
    don_id = request.form['don_id']
    don_amount = request.form['don_amount']
    don_time = request.form['don_time']
    db = pymysql.connect(host='localhost', port=3306, user='root', password='abc755716', db='care')
    cur = db.cursor()#设立游标
    if len(don) != 0:#判断是否输入
       #更新数据库
       sql3= "insert into inflow(donor,money_amount,record_time,donor_id) values(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE donor = VALUES(donor),money_amount = VALUES(money_amount),record_time = VALUES(record_time), donor_id= VALUES(donor_id);"
       param3 = (don,don_amount,don_time,don_id)
       cur.execute(sql3, param3)
       #flash消息提示
       flash("资金流入登记成功")
       db.commit()
       cur.close()
    else:print("未填入流入资金")

    #资金流出登记
    #获取输入的姓名，身份证号码，获助金额，获助时间以及资金去向
    rec_name = request.form['rec_name']
    rec_id = request.form['rec_id']
    rec_amount = request.form['rec_amount']
    rec_time = request.form['rec_time']
    rec_go = request.form['rec_go']
    if len(rec_name)!=0:#判断是否输入
       #更新数据库
       db = pymysql.connect(host='localhost', port=3306, user='root', password='abc755716', db='care')
       cur = db.cursor()  # 设立游标
       #更新outflow表中内容
       sql4 = "insert into outflow(recipient,money_amount,record_time,funds_go,recipient_id) values(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE recipient = VALUES(recipient),money_amount = VALUES(money_amount),record_time = VALUES(record_time), funds_go= VALUES(funds_go),recipient= VALUES(recipient);"
       param4 = (rec_name,rec_amount,rec_time,rec_go,rec_id)
       cur.execute(sql4,param4)
       #更新children表中c_assistance的内容，与outflow表中funds_go内容相同
       sql5 = "insert into children(c_id,c_assistance) values(%s,%s) ON DUPLICATE KEY UPDATE c_id=VALUES (c_id),c_assistance=VALUES (c_assistance);"
       param5 = (rec_id,rec_go)
       cur.execute(sql5,param5)
       db.commit()
       cur.close()
       #flash消息提示
       flash("资金流出登记与儿童援助情况更新成功")
    else:print("未填入流出资金")

    #儿童资格查询部分
    #获得输入的儿童身份证号码
    chi_id = request.form['chi_id']
    if len(chi_id) != 0:#判断是否输入
       #连接数据库
       db = pymysql.connect(host='localhost', port=3306, user='root', password='abc755716', db='care')
       cur = db.cursor()  # 设立游标
       #获得该身份证号码对应c_credit_level内容
       sql1="select c_credit_level from children where c_id =%s"
       cur.execute(sql1,chi_id)
       result1=cur.fetchone()
       result1= result1[0] #获得c_credit_level
       #获得该身份证号码对应的c_fortune内容
       sql2 = "select c_fortune from children where c_id=%s"
       cur.execute(sql2,chi_id)
       result2= cur.fetchone()
       result2 = result2[0] #获得c_fortune
       if result1 >= 2 and result2 <=3:#当c_credit_level不小于2并且c_fortune不大于3时，即符合受助资格
           flash('拥有资格')#flash消息提示
       else:
           flash('不符资格')#flash消息提示
       db.commit()
       cur.close()
    else:print("未填入身份证号码")
    return render_template('fulizijin.html')




if __name__ == '__main__':
    app.run()
