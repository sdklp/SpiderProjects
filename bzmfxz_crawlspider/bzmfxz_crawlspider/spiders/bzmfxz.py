import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
import re
from bzmfxz_crawlspider.items import BzmfxzCrawlspiderItem
import os

class BzmfxzSpider(CrawlSpider):
    name = 'bzmfxz'
    allowed_domains = ['bzmfxz.com']
    start_urls = ['http://www.bzmfxz.com/biaozhun/Soft/DLDLBZ/List_1.html']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/biaozhun/Soft/DLDLBZ/\d{4}.*\d\.html'), callback='parse_item'),   #文档列表
        # Rule(LinkExtractor(allow=r'/Common/ShowDownloadUrl\.aspx\?urlid=0&id=\d+'), callback='parse_doc'),  #下载页面，从中取Title和文档地址
        Rule(LinkExtractor(allow=r'/biaozhun/Soft/DLDLBZ/List_\d+\.html'), follow=True),  #分页
    )

    def parse_item(self, response):
        pattern=re.compile(r"window\.open\('(/Common/.*?\d+)'")
        url='http://www.bzmfxz.com/'+re.findall(pattern,response.body.decode())[0]
        yield Request(url=url,callback=self.parse_doc)


    def parse_doc(self,response):
        link=response.xpath("//div[@id='content']//a/@href").get()
        title=response.xpath("//h1[@class='STYLE1']/text()").get()
        if os.path.exists('download/'+ title + '.rar'):
            print(title + '.rar= = =已存在')
        else:
            item=BzmfxzCrawlspiderItem()
            item['file_urls']=[link]
            item['Title']=title
            print(title+'= = ='+link)
            yield item
