from operator import itemgetter
from scrapy.item import Item, Field

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Identity

class TakeVeryFirst(object):
    def __call__(self, values):
        return values[0]

class Proxy(Item):
    address = Field()
    port = Field()
    type = Field()
    ssl = Field()

class ProxyItemLoader(XPathItemLoader):
    default_input_processor = MapCompose(unicode.strip, unicode.lower)
    default_output_processor = TakeFirst()

    ssl_in = Identity()
    ssl_out = TakeVeryFirst()
    port_in = MapCompose(int)
