import pymysql
import json
import codecs
from xml.dom import minidom
import xlrd
import os
import pandas as pd


# 用于文件数据集成的类
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
    def insert_json(self, filename, c_id):
        data_json = json.load(codecs.open(filename, 'r', 'utf-8'))
        c_id = str(c_id)
        # 查询是否有该条数据
        sql1 = "SELECT * FROM {} WHERE `c_id` = %s".format("children")
        self.cursor.execute(sql1, c_id)
        data = self.cursor.fetchone()
        # 有则更新，无则插入
        if data:
            sql2 = "UPDATE {} SET `c_education`=%s,`c_loan`=%s,`c_school`=%s WHERE `c_id`={}".format('children', c_id)
            try:
                for i, data in enumerate(data_json):
                    if data['id'] == c_id:
                        self.cursor.execute(sql2, (data['education_level'], int(data['loan']), data['school']))
                        self.connect.commit()
                        print('json数据更新成功')
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
            except Exception as e:
                print('json_error: ', e)
        else:
            print("json发生其他错误！！！")

    def insert_xml(self, filename, c_id):
        c_id = str(c_id)
        # 建立数据暂存数组
        id_list = []
        name_list = []
        current_living_list = []
        actual_guardian_list = []
        domTree = minidom.parse(filename)
        # 文档根元素
        rootNode = domTree.documentElement
        # 所有顾客
        Rows = rootNode.getElementsByTagName("Row")

        try:
            for Row in Rows:
                # 身份证号元素
                id_num = Row.getElementsByTagName("身份证号")[0]
                id_list.insert(0, id_num.childNodes[0].data)
                if id_list[0] == c_id:
                    # 姓名元素
                    name = Row.getElementsByTagName("姓名")[0]
                    name_list.append(name.childNodes[0].data)
                    # 目前生活状况元素
                    current_living = Row.getElementsByTagName("目前生活状况")[0]
                    current_living_list.append(current_living.childNodes[0].data)
                    # 实际监护人元素
                    actual_guardian = Row.getElementsByTagName("实际监护人")[0]
                    actual_guardian_list.append(actual_guardian.childNodes[0].data)
                    self.cursor.execute(
                        'insert into children (c_id,c_name,c_living_condition,c_actual_guardian) values (%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE c_name=VALUES(c_name),c_living_condition=VALUES(c_living_condition),c_actual_guardian=VALUES(c_actual_guardian)',
                        [id_list[0], name_list[0], current_living_list[0], actual_guardian_list[0]])
                    self.connect.commit()
        except Exception as e:
            print('xml_error: ', e)

    def insert_csv(self, filename, c_id):
        c_id = int(c_id)
        # 用pandas读取csv
        data = pd.read_csv(filename, engine='python', encoding='utf-8')
        # 数据过滤，替换 nan 值为 None
        data = data.astype(object).where(pd.notnull(data), None)
        for id, gender, name, nation, b_p, b_c, date, edu_d, guard1, guard2, crime, children, c_p, c_c, social, age, actual in zip(
                data['身份证号'], data['性别'], data['姓名'], data['民族'], data['出生省'], data['出生市'], data['出生日期'], data['文化程度'],
                data['监护人一'], data['监护人二'], data['犯罪记录'], data['子女'],
                data['现居省'], data['现居市'], data['社会面貌'], data['年龄'], data['实际监护人']):
            if id == c_id:
                if int(age) < 18:
                    dataList = [id, gender, name, date, b_p, b_c, social,
                                guard1, guard2, c_p, c_c, actual, edu_d]
                    # print(dataList)  # 插入的值
                    try:
                        insertsql = "INSERT INTO children(c_id,c_gender,c_name,c_date,c_native_province,c_native_city,c_politics_status,c_guardian_one,c_guardian_two,c_current_province,c_current_city,c_actual_guardian,c_education) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        self.cursor.execute(insertsql, dataList)
                        self.connect.commit()
                        print("csv数据插入成功")
                    except Exception as e:
                        print("csv_error1:", e)
                        self.connect.rollback()
                else:
                    dataList = [id, name, gender, date, nation, b_p, b_c, edu_d,
                                children, crime, c_p, c_c]
                    # print(dataList)  # 插入的值
                    try:
                        insertsql = "INSERT INTO parents(p_id,p_name,p_gender,p_date,p_nation,p_native_province,p_native_city,p_education_degree,p_children,p_crime,p_current_province,p_current_city) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        self.cursor.execute(insertsql, dataList)
                        self.connect.commit()
                        print("csv数据插入成功")
                    except Exception as e:
                        print("csv_error2:", e)
                        self.connect.rollback()

    def insert_excel(self, filename, c_id):
        c_id = str(c_id)
        try:
            book = xlrd.open_workbook(filename)
        except:
            print("open excel file failed!")
        try:
            sheet = book.sheets()[0]  # execl里面的worksheet1
        except:
            print("locate worksheet in excel failed!")

        row_num = []
        value = {}
        row_num = sheet.nrows
        # i = 2
        for i in range(row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sheet.row_values(i)
            # print(row_data)
            value_1 = (row_data[0], row_data[6], row_data[7], row_data[8])
            value_2 = (row_data[0], row_data[7])
            if c_id == str(row_data[0]):
                sql_1 = "replace into children(`c_id`,`c_disability`,`c_health_level`,`c_health_care`) values(%s,%s,%s,%s)"
                sql_2 = "replace into parents(`p_id`,`p_health_level`) values(%s,%s)"
                self.cursor.execute(sql_1, value_1)  # 执行sql语句
                self.cursor.execute(sql_2, value_2)  # 执行sql语句
                self.connect.commit()

    def insert_txt(self, filename, c_id):
        c_id = str(c_id)
        file = open(filename, 'r')
        next(file)
        lines = file.readlines()

        if lines:
            for line in lines:
                line = line.strip('\n').split()
                child_id = line[0]
                gender = line[1]
                name = line[2]
                date = line[3]
                fortune = line[5]
                credit_level = line[4]
                if id == c_id:
                    # conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="abc755716", db="care")
                    # cursor = conn.cursor()
                    sql = "insert into children(c_id,c_gender,c_name,c_date,c_fortune,c_credit_level)values(%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE c_gender = VALUES(c_gender),c_name = VALUES(c_name),c_date = VALUES(c_date),c_fortune = VALUES(c_fortune),c_credit_level = VALUES(c_credit_level)"
                    param = (child_id, gender, name, date, fortune, credit_level)
                    self.cursor.execute(sql, param)
                    self.connect.commit()
                    print('txt数据更新成功')
        file.close()
        self.cursor.close()
        self.connect.close()


# 读入数据执行插入
def execute_insert(c_id):
    mysql = DataIntegrate()
    file_dir = "./static/data/"
    for root, dirs, files in os.walk(file_dir):
        for i, filename in enumerate(files):
            tmp_list = filename.split(".")
            t = tmp_list[1]
            if t == "csv":
                mysql.insert_csv(root + filename, c_id)
                print("csv数据插入成功")
            elif t == "json":
                mysql.insert_json(root + filename, c_id)
                print("json数据插入成功")
            elif t == "xlsx":
                mysql.insert_excel(root + filename, c_id)
                print("excel数据插入成功")
            elif t == "xml":
                mysql.insert_xml(root + filename, c_id)
                print("xml数据插入成功")
            elif t == "txt":
                mysql.insert_txt(root + filename, c_id)
                print("txt数据插入成功")
            else:
                print("这合理吗？")
    print("所有数据插入成功")


children_id = input()
execute_insert(children_id)
