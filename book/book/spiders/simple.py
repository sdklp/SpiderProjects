import scrapy


class SimpleSpider(scrapy.Spider):
    name = 'simple'
    start_urls = ['https://www.scrapebay.com/ebooks']
    
    

    def parse(self, response):
        
        for tag in response.xpath("//following::tr[4]/td[2]/a[not(contains(@href,'jpg'))]"):

            relative_url = tag.xpath(".//@href").extract_first()
            link = response.urljoin(relative_url)
            title =tag.xpath(".//text()").extract_first()
            yield {
                'Title': title,
                'file_urls': [link]
            }

