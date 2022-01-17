#coding=utf-8
import pymysql
class PythonMysql(object):
    # 构造方法
    def __init__(self,host,user,password,port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.mysql_db = self.connect_mysql()
    
    # 连接数据库
    def connect_mysql(self):
        try:
            mysql_db = pymysql.connect(host=self.host,
                                       user=self.user,
                                       password=self.password,
                                       port=self.port)
            print('数据库连接成功')
            return mysql_db
        except Exception as e:
            print(e)
            print('数据库连接失败')
            return None
        
    # 创建表
    def create_table(self,create_table_sql):
        try:
            cursor =  self.mysql_db.cursor()
            cursor.execute(create_table_sql)
            print('创建表成功')
        except Exception as e:
            print(e)
            print('创建表失败')
            
    # 查询数据
    def select_mysql(self,qurey_sql):
        cursor =  self.mysql_db.cursor()
        cursor.execute(qurey_sql)
        return self.mysql_db.cursor.fetchall()
    
    # 插入数据
    def insert_mysql(self,insert_sql):
        try:
            cursor =  self.mysql_db.cursor()
            cursor.execute(insert_sql)  # 执行插入语句
            self.mysql_db.commit() # commit方法跟在增删改查后面，意味着把语句提交给数据库
        except Exception as e:
            print(e)
            print(insert_sql)
            self.mysql_db.rollback()