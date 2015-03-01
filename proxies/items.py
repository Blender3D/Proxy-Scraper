from scrapy.item import Item, Field

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.exporter import BaseItemExporter
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

class Proxy(Item):
    address = Field()
    port = Field()

class ProxyItemLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
    
    address_in = MapCompose(unicode, unicode.strip)
    port_in = MapCompose(int)

class IPPortItemExporter(BaseItemExporter):
	def __init__(self, file, **kwargs):
		self._configure(kwargs, dont_fail=True)
		self.file = file

	def export_item(self, item):
		return self.file.write('{item[address]}:{item[port]}\n'.format(item=item))