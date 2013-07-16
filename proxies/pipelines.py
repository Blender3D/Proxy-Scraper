from scrapy.contrib.exporter import BaseItemExporter
from scrapy.exceptions import DropItem

class ProxiesPipeline(object):
    def process_item(self, item, spider):
        return item

class FlatFileItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file

    def export_item(self, item):
        self.file.write('{address}:{port}\n'.format(**item))