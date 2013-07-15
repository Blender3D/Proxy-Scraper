import urllib2
import socket
import time

from scrapy.exceptions import DropItem

def test_proxy(type, address):
    start = time.time()

    try:
        proxy_handler = urllib2.ProxyHandler({type: address})
        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Intel Mac OS X 10.6; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
        urllib2.install_opener(opener)

        request = urllib2.Request('http://example.iana.org/')
        connection = urllib2.urlopen(request, timeout=1.0)
        connection.close()
    except:
        return False, None

    return True, time.time() - start

class ProxiesPipeline(object):
    def process_item(self, item, spider):
        return item

    # Fake method
    def validate_item(self, item, spider):
        result, latency = test_proxy(item['type'], item['address'])

        if result and latency < 0.5:
            item['latency'] = latency

            return item
        else:
            raise DropItem