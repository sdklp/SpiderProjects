import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

#https://www.jb51.net/books/list45_1.html

class Job51SpiderSpider(CrawlSpider):
    name = 'job51_spider'
    allowed_domains = ['jb51.net']
    start_urls = ['https://www.jb51.net/do/book_class.html']

    rules = (
        Rule(LinkExtractor(allow=r'/books/\d+.html'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/books/list\d+_d+\.html')),

        Rule(LinkExtractor(allow=r'list\d+_\d+\.html'),follow=True)
    )

    def parse_item(self, response):
        # item = {}
        # print(response.url)
        title=response.xpath('//*[@id="download"]/ul/li[1]/h3/text()').get()
        link=response.xpath('//*[@id="download"]/ul/li[1]/ul[2]/li[1]/a[contains(@href,"rar")]/@href').get()
        print(link)
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # yield {
        #     "title":title,
        #     "file_urls":[link]
        # }
