# -*- coding: utf-8 -*-

from xml.dom import minidom
import pymysql

def Import_research_record(input_ID=''):
    # 建立数据暂存数组
    IDnum_list = []
    name_list = []
    current_living_list = []
    actual_guardian_list = []

    domTree = minidom.parse('../调查数据.xml')
    # 文档根元素
    rootNode = domTree.documentElement

    # 所有顾客
    Rows = rootNode.getElementsByTagName("Row")

    for Row in Rows:
        # 身份证号元素
        IDnum = Row.getElementsByTagName("身份证号")[0]
        IDnum_list.insert(0,IDnum.childNodes[0].data)
        if IDnum_list[0] == input_ID:
            # 姓名元素
            name = Row.getElementsByTagName("姓名")[0]
            name_list.append(name.childNodes[0].data)
            # 目前生活状况元素
            current_living = Row.getElementsByTagName("目前生活状况")[0]
            current_living_list.append(current_living.childNodes[0].data)
            # 实际监护人元素
            actual_guardian = Row.getElementsByTagName("实际监护人")[0]
            actual_guardian_list.append(actual_guardian.childNodes[0].data)
            #导入数据库
            conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="dqy5240138", db="care")
            cursor = conn.cursor()
            cursor.execute('insert into children (c_id,c_name,c_living_condition,c_actual_guardian) values (%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE c_name=VALUES(c_name),c_id=VALUES(c_id),c_living_condition=VALUES(c_living_condition),c_actual_guardian=VALUES(c_actual_guardian)', [IDnum_list[0],name_list[0],current_living_list[0],actual_guardian_list[0]])
            conn.commit()
            cursor.close()

if __name__ == '__main__':
    Import_research_record('862112842654896000')