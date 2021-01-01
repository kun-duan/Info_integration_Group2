import pymysql
import data_integrate


# 将申请人的信息插入
def user_apply(p_id, p_phone_number, p_audit_status):
    data_integrate.execute_insert(p_id)
    connect = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="care", charset='utf8')
    cursor = connect.cursor()
    sql = "UPDATE parents SET `p_phone_number` =%s,`p_audit_status` = %s WHERE `p_id`={}".format(p_id)
    cursor.execute(sql, (p_phone_number, p_audit_status))
    connect.commit()
    # print("领养登记成功")
    cursor.close()
    connect.close()


# 过滤出不符合申请条件的人
def user_filter(p_id):
    connect = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="care", charset='utf8')
    cursor = connect.cursor()
    sql = "SELECT `p_crime`,`p_credit_level`,`p_health_level` FROM parents WHERE `p_id` = %s"
    cursor.execute(sql, p_id)
    select_data = cursor.fetchall()
    if select_data[0][0] == "有":
        return True  # 返回True表示申请失败
    elif int(select_data[0][1]) < 3:
        return True
    elif select_data[0][2] == "残疾" or "较差":
        return True
    else:
        return False


# 如果不满足要求修改申请状态为申请失败
def update_status(p_id):
    p_audit_status = "申请失败"
    connect = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="care", charset='utf8')
    cursor = connect.cursor()
    sql = "UPDATE parents SET `p_audit_status` = %s WHERE `p_id`={}".format(p_id)
    cursor.execute(sql, p_audit_status)
    connect.commit()
    cursor.close()
    connect.close()


# 用户搜索信息
def user_search(query):
    connect = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="care", charset='utf8')
    cursor = connect.cursor()
    sql = "SELECT `p_name`,`p_gender`,`p_nation`,`p_audit_status` FROM parents WHERE `p_id` = %s"
    cursor.execute(sql, query)
    select_tmp = cursor.fetchall()
    select_data = list(select_tmp[0])
    if len(select_data) == 0:
        return "查无此人"
    elif len(select_data) > 0:
        return select_data
    cursor.close()
    connect.close()


# 管理员登记
def governor_register(p_id, p_children_id, p_status):
    connect = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="care", charset='utf8')
    cursor = connect.cursor()
    sql = "UPDATE parents SET `p_audit_status`=%s,`p_children_id`=%s WHERE `p_id`={}".format(p_id)
    cursor.execute(sql, (p_status, p_children_id))
    connect.commit()

    cursor.close()
    connect.close()


# 管理员搜索
def governor_search(query):
    connect = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="care", charset='utf8')
    cursor = connect.cursor()
    sql = "SELECT `p_id`,`p_name`,`p_gender`,`p_date`,`p_nation`,`p_education_degree`,`p_children`,`p_crime`,`p_current_city`,`p_credit_level`,`p_health_level`,`p_audit_status`,`p_phone_number`,`p_children_id` FROM parents WHERE `p_id` = %s or `p_name` = %s or `p_children_id` = %s "
    cursor.execute(sql, (query, query, query))
    select_tmp = cursor.fetchall()
    select_data = list(select_tmp[0])
    if len(select_data) == 0:
        return "查无此人"
    elif len(select_data) > 0:
        return select_data
    cursor.close()
    connect.close()

