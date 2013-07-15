import urllib2
import socket
import time

from scrapy.exceptions import DropItem

class ProxiesPipeline(object):
    HTTP_PROXIES = frozenset([
        'http',
        'https',
        'transparent',
        'elite',
        'high',
        'anonymous',
        'distorting'
    ])

    def process_item(self, item, spider):
        type = item['type']

        if type in self.HTTP_PROXIES:
            item['type'] = 'http'

            if 'ssl' not in item:
                item['ssl'] = False
        elif '5' in type:
            item['type'] = 'socks5'
            item['ssl'] = True
        elif '4' in type:
            item['type'] = 'socks4'
            item['ssl'] = True
        else:
            raise DropItem

        return item
