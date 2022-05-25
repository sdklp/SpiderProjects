# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from jb51.items import Jb51Item

class MyPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        name=item.get("title")
        suffix=str(item.get('file_urls')[0]).split(".")[-1]
        return name+".rar"

class Jb51Pipeline:
    def process_item(self, item, spider):
        return item
