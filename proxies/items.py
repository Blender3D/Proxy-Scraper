from scrapy.item import Item, Field

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Identity

class Proxy(Item):
    address = Field()
    port = Field()
    type = Field()
    latency = Field()

class ProxyItemLoader(XPathItemLoader):
    default_output_processor = TakeFirst()

    address_in = Identity()
    port_in = MapCompose(int)
    type_in = MapCompose(unicode.lower)