import scrapy


class BzmfxzSpiderSpider(scrapy.Spider):
    name = 'bzmfxz_spider'
    allowed_domains = ['bzmfxz.com']
    start_urls = ['http://bzmfxz.com/']

    def parse(self, response):
        pass
