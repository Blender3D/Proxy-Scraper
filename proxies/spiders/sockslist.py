from proxyhttp import ProxyhttpSpider

class SocksListSpider(ProxyhttpSpider):
    name = 'sockslist'
    allowed_domains = ['sockslist.net']
    start_urls = ['http://sockslist.net/']