import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bzmfxz.items import BzmfxzItem


class BzmfxzSpiderSpider(CrawlSpider):
    name = 'bzmfxz_spider'
    allowed_domains = ['bzmfxz.com']
    #电力标准列表
    start_urls = ['http://www.bzmfxz.com/biaozhun/Soft/DLDLBZ/List_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/biaozhun/Soft/DLDLBZ/\d{4}.*\d\.html'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/biaozhun/Soft/DLDLBZ/List_\d\.html'),  follow=True),
    )

    def parse_item(self, response):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'Referer':response.url
        }
        url='http://www.bzmfxz.com/Common/ShowDownloadUrl.aspx?urlid=0&id='+response.url.split('/')[-1].split('.')[0]

        yield scrapy.Request(url=url,callback=self.parse_document,headers=headers)


    def parse_document(self,response):
        title=file_url=response.xpath("//h1[@class='STYLE1']/text()").get()
        link=response.xpath("//div[@id='content']//a/@href").get()
        item=BzmfxzItem()
        item['Title']=title
        item['file_urls']=[link]
        print(title+'---'+link)
        yield item