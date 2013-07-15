from scrapy.item import Item, Field

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

class Proxy(Item):
    address = Field()
    port = Field()

class ProxyItemLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
    
    address_in = MapCompose(unicode.strip)
    port_in = MapCompose(int)