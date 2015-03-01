import operator

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from proxies.items import Proxy, ProxyItemLoader

class XroxySpider(CrawlSpider):
    name = 'xroxy'
    allowed_domains = ['www.xroxy.com']
    start_urls = ['http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum=0']

    rules = (
        Rule(
            SgmlLinkExtractor(
                restrict_xpaths='//table[@class="tbl"]',
                allow=r'/proxylist\.php'
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_page(self, response):
        xpath = HtmlXPathSelector(response)

        for row in xpath.select('//table[@cellpadding="3"]/tr[starts-with(@class, "row")]'):
            loader = ProxyItemLoader(item=Proxy(), response=response, selector=row)
            
            loader.add_xpath('port', 'td[3]/a/text()')
            loader.add_xpath('address', 'td[2]/a/text()')

            yield loader.load_item()