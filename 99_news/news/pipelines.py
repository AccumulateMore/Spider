#coding=utf-8
from itemadapter import ItemAdapter
from news.mysql_operater import PythonMysql # mysql_operater.py 在news文件夹下
import csv 
import pymongo

class NewsPipeline:
    def __init__(self):
        self.filename = 'news.csv'
        
    def process_item(self,item,spider):    
        self.write_csv(item)
        return item
    
    def write_csv(self,dictdata):
        with open(self.filename,'a',encoding='utf-8-sig',newline='') as csvf:             
            fieldnames = ['title','new_url','abstract','new_type','date','image_url','new_content']        
            writer = csv.DictWriter(csvf,fieldnames=fieldnames)                                  
            writer.writerow(dictdata)   
        
class MysqlPipeline:
    def __init__(self):
        self.mysql = PythonMysql(host='localhost',user='root',password='password',port=3306)                  
        self.create_sql = '''
                          create table if not exists ai.news_data
                           (
                           title varchar(500) comment '新闻名',   
                           new_url varchar(100) comment '新闻链接',
                           abstract text comment '摘要',
                           new_type varchar(150) comment '新闻类型',
                           date varchar(100) comment '新闻发布日期',
                           image_url varchar(100) comment '图片链接'
                           )
                          '''
        self.mysql.create_table(self.create_sql) # 在初始化中创建表
        
    def process_item(self,item,spider):
        insert_sql = '''
                     insert into ai.news_data values('{}','{}','{}','{}','{}','{}')
                     '''                                 
        insert_sql = insert_sql.format(item['title'],
                                       item['new_url'],
                                       item['abstract'],
                                       item['new_type'],
                                       item['date'],
                                       item['image_url'])
        self.mysql.insert_mysql(insert_sql)
        return item   
    
class MongodbPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost',port=27017)
        self.db = self.client.scrapy_data
        self.collection = self.db.news_data
        
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item 