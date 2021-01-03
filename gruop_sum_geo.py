
# -*- coding: UTF-8 -*-
import pymysql
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import random

class renew_sql:
 def get_geo_sql(self):
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",password="1234",
                         db="care",charset="utf8")

    cursor = conn.cursor()
    sql="SELECT c_current_province,count(*) AS sum_children FROM children group by c_current_province"
    sql_2="SELECT p_current_province,count(*) AS sum_parents FROM parents group by p_current_province"
    epidemic = pd.read_sql(sql, con=conn)
# print(epidemic)
    data=epidemic.values
    epidemic_2 = pd.read_sql(sql_2, con=conn)
# print(epidemic_2)
    data_2=epidemic_2.values
# print(data_2)
# cursor.execute(sql)
# cursor.execute(sql_2)
# data=cursor.fetchall()
# data_2=cursor.fetchall()


# geodata = []
# for i in range(len(data)):
#     print(data[i][0])
#     for j in range(len(data_2)):
#         if(data[i][0]==data_2[j][0]):
#             geodata.append(data[i][0],data[i][1],data_2[j][1])
#         else:
#             if
# print(geodata)

    geo_data1 = DataFrame(data)
# print(geo_data1)
    geo_data2 = DataFrame(data_2)
# print(geo_data2)

    merge_data = pd.merge(geo_data1, geo_data2, left_on=0, right_on=0, how='outer')
# print(merge_data)
    all_data = []
# print(merge_data["1_x"][2])
    for i in range(len(merge_data[0])):
    # print(merge_data[0][i])
      if(np.isnan(merge_data["1_x"][i])==None):
        merge_data["1_x"][i]=0
      all_data.append((merge_data[0][i], merge_data["1_x"][i], merge_data["1_y"][i]))
# print(all_data)
    t = np.asarray(all_data)
    covert = np.nan_to_num(t)
# print(covert)

    for i in range(len(covert)):
      for j in range(len(covert[i])):
        # print(covert[i][j])
        if covert[i][j] == 'nan':
            covert[i][j] = 0
    print(covert)
# list_covert=np.array(covert)
# print(type(list_covert))
# print(list_covert)
# data11=[]
# data22=[]
# for i in range(len(list_covert)):
#     for j in range(len(list_covert[i])):
#         # print(covert[i][j])
#         if(j==1):
#             data1 = np.array(list(map(int, list_covert[i][j])))
#             print(data1)
#             print(type(data1))
#             data11.append(data1)
#         elif(j==2):
#             data2 = np.array(list(map(int, list_covert[i][j])))
# print(data11)
    list_values = []
    for i in range(0, len(covert)):
       list_values.append(list(covert[i]))
    print(list_values)
    tuple_data=tuple(list_values)
    print(tuple_data[1])
    for i in range(len(list_values)):
        sql_3 = "replace into geoinformation(`province`,`sum_children`,`sum_parents`) values(%s,%s,%s)"
        cursor.execute(sql_3, tuple_data[i]) # 执行sql语句
    conn.commit()
    sql_4="SELECT * FROM geoinformation"
    epidemic_4=pd.read_sql(sql_4,con=conn)
    data_4=epidemic_4.values
    print(data_4)

    for i in range(len(data_4)):
        for j in range(len(data_4[i])):
            if(j==1):
              if(data_4[i][j]==0):
                number=random.uniform(1000,20000)
                data_4[i][j]=int((data_4[i][j]+1)*number)
              else:
                number_2=random.uniform(2000,4000)
                data_4[i][j]=int(data_4[i][j]*number_2)
            elif(j==2):
              if(data_4[i][j]==0):
                number_3=random.uniform(1000,10000)
                data_4[i][j]=int((data_4[i][j]+1)*number_3)
              else:
                number_4=random.uniform(2000,4000)
                data_4[i][j]=int(data_4[i][j]*number_4)
    list_values_2 = []
    for i in range(0, len(data_4)):
        list_values_2.append(list(data_4[i]))
    for i in range(len(list_values_2)):
        sql_5 = "replace into geoinformation(`province`,`sum_children`,`sum_parents`,`bilv`) values(%s,%s,%s,%s)"
        cursor.execute(sql_5, list_values_2[i])
    conn.commit()
    cursor.close()
    return data_4
if __name__=="__main__":
    u=renew_sql()
    print(u.get_geo_sql())