import pymysql


def user_search(query):
    connect = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="care", charset='utf8')
    cursor = connect.cursor()
    sql = "SELECT `p_name`,`p_gender`,`p_nation`,`p_audit_status` FROM parents WHERE `p_id` = %s"
    cursor.execute(sql, query)
    select_data = cursor.fetchall()
    if len(select_data) == 0:
        return "查无此人"
    elif len(select_data) > 0:
        return select_data
    cursor.close()
    connect.close()


q = "423561235869475000"
print(user_search(q))
