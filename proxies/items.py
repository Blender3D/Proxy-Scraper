from scrapy.item import Item, Field

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Identity

class Proxy(Item):
    address = Field()
    port = Field()
    type = Field()
    latency = Field()

class ProxyItemLoader(XPathItemLoader):
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

    port_in = MapCompose(int)
    type_in = MapCompose(unicode.lower)