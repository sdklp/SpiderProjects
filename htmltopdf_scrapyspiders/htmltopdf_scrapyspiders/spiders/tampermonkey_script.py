import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TampermonkeyScriptSpider(CrawlSpider):
    name = 'tampermonkey_script'
    # allowed_domains = ['tampermonkey.net.cn']
    start_urls = ['https://bbs.tampermonkey.net.cn/thread-184-1-1.html']

    rules = (
        # Rule(LinkExtractor(allow=r'https://bbs.tampermonkey.net.cn/thread-\d+-1-1\.html'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="postmessage_826"]/a'),callback='parse_item'),
    )

    def parse_item(self, response):
        # item = {}
        print(response.url)
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        # return item


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl tampermonkey_script --nolog".split())