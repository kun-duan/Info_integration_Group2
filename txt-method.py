import pymysql


def insert_mysql_txt(input_ID=''):
    input_ID2 = str(input_ID)
    file = open("C:/Users/Lenovo/Desktop/银行.txt", 'r')
    next(file)
    lines = file.readlines()

    if lines:
        for line in lines:
            if not line.strip(): continue
            line = line.strip('\n').split()
            id = line[0]
            gender = line[1]
            name = line[2]
            date = line[3]
            fortune = line[5]
            credit_level = line[4]
            age1 = line[6]
            age2 = int(age1)
            if id == input_ID2:
                conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="dqy5240138", db="care")
                cursor = conn.cursor()
                if age2 > 18:
                    sql = "insert into parents(p_id,p_gender,p_name,p_date,p_fortune,p_credit_level)values(%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE p_id = VALUES(p_id),p_gender = VALUES(p_gender),p_name = VALUES(p_name),p_date = VALUES(p_date),p_fortune = VALUES(p_fortune),p_credit_level = VALUES(p_credit_level)"
                    param = (id, gender, name, date, fortune, credit_level)
                    cursor.execute(sql, param)
                    conn.commit()
                    file.close()
                    cursor.close()
                    conn.close()
                    print('父母数据更新成功')
                else:
                    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="dqy5240138", db="care")
                    cursor = conn.cursor()
                    sql = "insert into children(c_id,c_gender,c_name,c_date,c_fortune,c_credit_level)values(%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE c_id = VALUES(c_id),c_gender = VALUES(c_gender),c_name = VALUES(c_name),c_date = VALUES(c_date),c_fortune = VALUES(c_fortune),c_credit_level = VALUES(c_credit_level)"
                    param = (id, gender, name, date, fortune, credit_level)
                    cursor.execute(sql, param)
                    conn.commit()
                    file.close()
                    cursor.close()
                    conn.close()
                    print('孩子数据更新成功')

