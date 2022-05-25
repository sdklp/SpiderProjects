from scrapy_redis.spiders import RedisSpider
import scrapy

class Bzmfxz(RedisSpider):
    name = 'bzmfxz'
    allowed_domains = ['bzmfxz.com']
    #http://www.bzmfxz.com/biaozhun/Soft/DLDLBZ/List_1.html
    # start_urls=['http://www.bzmfxz.com/biaozhun/Soft/DLDLBZ/List_1.html']
    redis_key = 'bzmfxz:start_urls'

    def parse(self, response):
        print(response.url)