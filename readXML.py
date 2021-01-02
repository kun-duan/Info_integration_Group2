# -*- coding: utf-8 -*-
#解析XML
from xml.dom import minidom
import pymysql

#建立数据暂存数组
IDnum_list = []
name_list = []
current_living_list = []
actual_guardian_list = []

def readXML(filepath):
    domTree = minidom.parse(filepath)
	# 文档根元素
    rootNode = domTree.documentElement

	# 所有顾客
    Rows = rootNode.getElementsByTagName("Row")

    for Row in Rows:
        #身份证号元素
        IDnum = Row.getElementsByTagName("身份证号")[0]
        IDnum_list.append(IDnum.childNodes[0].data)
        #姓名元素
        name = Row.getElementsByTagName("姓名")[0]
        name_list.append(name.childNodes[0].data)
        #目前生活状况元素
        current_living = Row.getElementsByTagName("目前生活状况")[0]
        current_living_list.append(current_living.childNodes[0].data)
        #实际监护人元素
        actual_guardian = Row.getElementsByTagName("实际监护人")[0]
        actual_guardian_list.append(actual_guardian.childNodes[0].data)


def insert_to_DB():
    for i in range(0,len(IDnum_list)-1):
        #创建数据库链接
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="dqy5240138", db="care")
        cursor = conn.cursor()
        cursor.execute('insert into children (c_id,c_name,c_living_condition,c_actual_guardian) values (%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE c_name=VALUES(c_name),c_id=VALUES(c_id)', [IDnum_list[i],name_list[i],current_living_list[i],actual_guardian_list[i]])
        conn.commit()
        cursor.close()


if __name__ == '__main__':
    readXML('../static/data/调查数据.xml')
    insert_to_DB()

