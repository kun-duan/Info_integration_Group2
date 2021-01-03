from xml.dom import minidom
import pymysql


def data_query(key_value):
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="dqy5240138", db="care")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM care.children WHERE c_id=%s || c_name=%s', [key_value, key_value])
    res = cursor.fetchone()
    conn.commit()
    cursor.close()
    return res


def insert_type(tub_val):
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="dqy5240138", db="care")
    cursor = conn.cursor()
    cursor.execute('insert into children (c_id,c_type) values (%s,%s)  ON DUPLICATE KEY UPDATE c_type=VALUES(c_type), c_id=VALUES(c_id)', [tub_val[0],tub_val[1]])
    conn.commit()
    cursor.close()