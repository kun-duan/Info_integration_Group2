import pymysql
from sqlalchemy import create_engine
import pandas as pd
import datetime


class utils_ertong:
    def __init__(self,db_name,table_name,user,password):
        self.db_name=db_name
        self.table_name=table_name
        self.user=user
        self.password=password
        self.data = self.querry()
    def get_conn(self):
        '''

        :return:连接
        '''
        #创建连接
        conn=pymysql.connect(host="127.0.0.1",port=3306,user=self.user,password=self.password,
                             db=self.db_name,charset="utf8")
        cursor=conn.cursor()
        return conn,cursor

    def close_conn(self,conn,cursor):
        cursor.close()
        conn.close()

    def querry(self):
        #使用pandas从数据库中读取疫情数据
        conn = create_engine('mysql://{}:{}@localhost:3306/{}?charset=utf8'.format(self.user,self.password,self.db_name))
        sql="SELECT province,sum_children FROM {}".format(self.table_name)
        epidemic = pd.read_sql(sql, con=conn)
        return epidemic

    def get_c2_data(self):
        '''
        获取中国各省的疫情数据
        :return:
        '''
        #将地区-确诊人数以键值对的形式保存
        dict={}

        # 获取最新数据
        # 由于接口数据只能拿到前一天，因此我们的日期数据应该-1天
        df=self.data

        for p,v in zip(df.province,df.sum_children):
            dict[p]=v
        return dict

class utils_fumu:
    def __init__(self,db_name,table_name,user,password):
        self.db_name=db_name
        self.table_name=table_name
        self.user=user
        self.password=password
        self.data = self.querry()
    def get_conn(self):
        '''

        :return:连接
        '''
        #创建连接
        conn=pymysql.connect(host="127.0.0.1",port=3306,user=self.user,password=self.password,
                             db=self.db_name,charset="utf8")
        cursor=conn.cursor()
        return conn,cursor

    def close_conn(self,conn,cursor):
        cursor.close()
        conn.close()

    def querry(self):
        #使用pandas从数据库中读取疫情数据
        conn = create_engine('mysql://{}:{}@localhost:3306/{}?charset=utf8'.format(self.user,self.password,self.db_name))
        sql="SELECT province,sum_parents FROM {}".format(self.table_name)
        epidemic = pd.read_sql(sql, con=conn)
        return epidemic

    def get_c2_data_fumu(self):
        '''
        获取中国各省的疫情数据
        :return:
        '''
        #将地区-确诊人数以键值对的形式保存
        dict={}

        # 获取最新数据
        # 由于接口数据只能拿到前一天，因此我们的日期数据应该-1天
        df=self.data

        for p,v in zip(df.province,df.sum_parents):
            dict[p]=v
        return dict

class utils_lingyanglv:
    def __init__(self,db_name,table_name,user,password):
        self.db_name=db_name
        self.table_name=table_name
        self.user=user
        self.password=password
        self.data = self.querry()
    def get_conn(self):
        '''

        :return:连接
        '''
        #创建连接
        conn=pymysql.connect(host="127.0.0.1",port=3306,user=self.user,password=self.password,
                             db=self.db_name,charset="utf8")
        cursor=conn.cursor()
        return conn,cursor

    def close_conn(self,conn,cursor):
        cursor.close()
        conn.close()

    def querry(self):
        #使用pandas从数据库中读取疫情数据
        conn = create_engine('mysql://{}:{}@localhost:3306/{}?charset=utf8'.format(self.user,self.password,self.db_name))
        sql="SELECT province,(sum_parents/sum_children)*1.0 bilv FROM {}".format(self.table_name)
        epidemic = pd.read_sql(sql, con=conn)

        return epidemic

    def get_r1_data(self):
        '''
        获取中国各省的疫情数据
        :return:
        '''
        #将地区-确诊人数以键值对的形式保存
        dict={}

        # 获取最新数据
        # 由于接口数据只能拿到前一天，因此我们的日期数据应该-1天
        df=self.data
        df=df.sort_values(by='bilv',ascending=False)[:6]
        print(df)
        for p,v in zip(df.province,df.bilv):
            dict[p]=v
        return dict



if __name__=="__main__":
    u=utils_lingyanglv("care","geoinformation","root","1234")
    print(dict(u.get_r1_data()))

