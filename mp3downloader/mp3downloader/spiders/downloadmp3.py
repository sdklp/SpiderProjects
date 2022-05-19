import scrapy
from scrapy.loader import ItemLoader
from mp3downloader.items import Mp3DownloaderItem

class Downloadmp3Spider(scrapy.Spider):
    name = 'downloadmp3'

    start_urls = ['http://195.122.253.112/public/mp3/Metallica/Albums/1996%20-%20Load/']

    def parse(self, response):
        for link in response.xpath("//following::tr[4]/td[2]/a[not(contains(@href,'jpg'))]"):
            loader=ItemLoader(item=Mp3DownloaderItem(),selector=link)
            relative_url=link.xpath(".//@href").extract_first()
            absolute_url=response.urljoin(relative_url)
            loader.add_value('file_urls',absolute_url)
            yield loader.load_item()


