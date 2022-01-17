# 这是setting.py 文件(设置爬虫配准)

BOT_NAME = 'news'

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # 为True表示遵守 ROBOST 协议，为False表示不遵守 ROBOST 协议
                        # ROBOST 协议即别人不允许你爬的，你爬的话会自动报错。

DEFAULT_REQUEST_HEADERS = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}
# 这里用的是豆瓣头文件覆盖的原内容

ITEM_PIPELINES = {
    'news.pipelines.NewsPipeline': 300, 
    'news.pipelines.MysqlPipeline': 301, 
    'news.pipelines.MongodbPipeline': 302
}

FEED_EXPORT_ENCODING = 'utf-8'