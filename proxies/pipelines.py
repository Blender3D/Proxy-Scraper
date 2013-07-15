from scrapy.exceptions import DropItem

class ProxiesPipeline(object):
    def process_item(self, item, spider):
        return item
