#coding=utf-8
import scrapy 
from news.items import NewsItem
import requests
from lxml import etree
import re
import os

class TouzijieSpider(scrapy.Spider):
    name = 'touzijie'
    allowed_domains = ['pe.pedaily.cn']
    
    # 方法2：字符串替换实现翻页
    start_urls = ['https://pe.pedaily.cn/vcpe/1/']
    page = 1  # 类属性 用self.page 调用

    dir_name = r'.\content'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        
    def parse(self, response):
        news = response.xpath('//*[@id="newslist-all"]/li')
        for new in news:
            new_item = NewsItem()
            new_item['title'] = new.xpath('./div[2]/h3/a/text()').extract_first()     
            new_item['new_url'] = new.xpath('./div[2]/h3/a/@href').extract_first()                        
            new_item['abstract'] = new.xpath('./div[2]/div[1]/text()').extract_first()       
            new_types = new.xpath('./div[2]/div[2]/a')    
            new_item['new_type'] = ','.join([types.xpath('./text()').extract_first() for types in new_types])               
            new_item['date'] = new.xpath('./div[2]/div[2]/span/text()').extract_first()    
            new_item['image_url'] = new.xpath('./div[1]/a/img/@src').extract_first()  
            if new_item['new_url']:
                new_item["new_content"] = self.content(new_item['new_url'])    
            yield new_item
            
        print('当前的url：',response.url)
        next_url = response.url.replace(str(self.page),str(self.page+1))  #类属性要用self去调用           
        print('下一页url：',next_url)
        self.page += 1
        if self.page>100:
            pass
        else:
            yield scrapy.Request(url=next_url,callback=self.parse)
            
    def content(self,url):
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",   
            "Accept-Encoding":"gzip, deflate, br",  
            "Accept-Language":"zh-CN,zh;q=0.9",   
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"     
        }
        if url:
            res = requests.get(url,headers = headers)
            res.encoding = 'utf-8'
            html = etree.HTML(res.text)
            duanluos = html.xpath('//*[@id="news-content"]/p')
            if duanluos:
                content = '\n'.join([duanluo.xpath('./text()')[0] for duanluo in duanluos if duanluo.xpath('./text()')])     
        return content