import scrapy 
class NewsItem(scrapy.Item):
    title = scrapy.Field()
    new_url = scrapy.Field()
    abstract = scrapy.Field()
    new_type = scrapy.Field()
    date = scrapy.Field()
    image_url = scrapy.Field()
    new_content = scrapy.Field()