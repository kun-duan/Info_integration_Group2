import pymysql
import json
import codecs
import pandas as pd


# 用于数据集成的类
class DataIntegrate:
    def __init__(self):
        # MySQL
        self.MYSQL_HOST = 'localhost'
        self.MYSQL_DB = 'care'
        self.MYSQL_USER = 'root'
        self.MYSQL_PWD = '123456'
        self.connect = pymysql.connect(
            host=self.MYSQL_HOST,
            db=self.MYSQL_DB,
            port=3306,
            user=self.MYSQL_USER,
            passwd=self.MYSQL_PWD,
            charset='utf8',
            use_unicode=False
        )
        print(self.connect)
        self.cursor = self.connect.cursor()

    # 插入数据的主函数
    def insert_mysql_json(self, data_json, c_id):
        c_id = str(c_id)
        sql1 = "SELECT * FROM {} WHERE `c_id` = %s".format("children")
        self.cursor.execute(sql1, c_id)
        data = self.cursor.fetchone()
        if data:
            sql2 = "UPDATE {} SET `c_education`=%s,`c_loan`=%s,`c_school`=%s WHERE `c_id`={}".format('children', c_id)
            try:
                for i, data in enumerate(data_json):
                    if data['id'] == c_id:
                        self.cursor.execute(sql2, (data['education_level'], int(data['loan']), data['school']))
                        self.connect.commit()
                        print('数据更新成功')
            except Exception as e:
                print('error: ', e)
        elif not data:
            sql3 = "insert into {}(`c_id`, `c_education`, `c_loan`, `c_school`) VALUES (%s, %s, %s, %s)".format(
                'children')
            try:
                for i, data in enumerate(data_json):
                    if data['id'] == c_id:
                        self.cursor.execute(sql3, (data['id'], data['education_level'], int(data['loan']),
                                                   data['school']))
                        self.connect.commit()
                        print('数据插入成功')
            except Exception as e:
                print('error: ', e)
        else:
            print("发生其他错误！！！")


# 读入数据执行插入
def execute_insert(c_id):
    mysql = DataIntegrate()
    data_json = json.load(codecs.open('./static/data/教育部.json', 'r', 'utf-8'))
    mysql.insert_mysql_json(data_json, c_id)


children_id = input()
execute_insert(children_id)
