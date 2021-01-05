# -*- coding: UTF-8 -*-
import pymysql
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np


class renew_sql:
 def get_geo_sql(self):
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",password="dqy5240138",
                         db="care",charset="utf8")
    cursor = conn.cursor()
    sql="SELECT c_current_province,count(*) AS sum_children FROM children group by c_current_province"
    sql_2="SELECT p_current_province,count(*) AS sum_parents FROM parents group by p_current_province"
    epidemic = pd.read_sql(sql, con=conn)
    data=epidemic.values
    epidemic_2 = pd.read_sql(sql_2, con=conn)
    data_2=epidemic_2.values
    #print(data_2)
    geo_data1 = DataFrame(data)
    geo_data2 = DataFrame(data_2)
    merge_data = pd.merge(geo_data1, geo_data2, left_on=0, right_on=0, how='outer')
    all_data = []
    for i in range(len(merge_data[0])):
      all_data.append((merge_data[0][i], merge_data["1_x"][i], merge_data["1_y"][i]))
    t = np.asarray(all_data)
    covert = np.nan_to_num(t)

    for i in range(len(covert)):
      for j in range(len(covert[i])):
        # print(covert[i][j])
        if covert[i][j] == 'nan':
            covert[i][j] = 0
    #print(covert)
    list_values = []
    for i in range(0, len(covert)):
       list_values.append(list(covert[i]))
    tuple_data=tuple(list_values)
    sql_6="delete from geoinformation"
    cursor.execute(sql_6)
    conn.commit()
    for i in range(len(tuple_data)):
        sql_3 = "insert into geoinformation(`province`,`sum_children`,`sum_parents`) values(%s,%s,%s) "
        cursor.execute(sql_3, tuple_data[i])
    conn.commit()
    #sql_6 = "delete from geoinformation where province='广东'"
    #cursor.execute(sql_6)
    #conn.commit()
    sql_4="SELECT * FROM geoinformation"

    epidemic_4=pd.read_sql(sql_4,con=conn)
    data_4=epidemic_4.values

    for i in range(len(data_4)):
        for j in range(len(data_4[i])):
            if(j==1):
              if(data_4[i][j]==0):
                data_4[i][j]=int((data_4[i][j]+1)*2333)
              else:
                data_4[i][j]=int(data_4[i][j]*5789)
            elif(j==2):
              if(data_4[i][j]==0):
                data_4[i][j]=int((data_4[i][j]+1)*4666)
              else:
                data_4[i][j]=int(data_4[i][j]*6539)
    list_values_2 = []
    for i in range(0, len(data_4)):
        list_values_2.append(list(data_4[i]))
    for i in range(len(list_values_2)):
        sql_5 = "replace into geoinformation(`province`,`sum_children`,`sum_parents`,`bilv`) values(% s,% s,% s,% s)"
        cursor.execute(sql_5, list_values_2[i])
    conn.commit()
    cursor.close()
    return data_4
if __name__=="__main__":
    u=renew_sql()
    print(u.get_geo_sql())