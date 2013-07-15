import operator

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from proxies.items import Proxy, ProxyItemLoader

class CoolProxySpider(CrawlSpider):
    name = 'coolproxy'
    allowed_domains = ['www.cool-proxy.net']
    start_urls = ['http://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc']

    rules = (
        Rule(
            SgmlLinkExtractor(
                restrict_xpaths='//th[@class="pagination"]'
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_page(self, response):
        xpath = HtmlXPathSelector(response)

        for row in xpath.select('//table/tr[count(td) > 1]')[1:-1]:
            loader = ProxyItemLoader(item=Proxy(), response=response, selector=row)

            address = row.select('td[1]/script/text()').re(r'"(.*?)"')[0].decode('base64')
            loader.add_value('address', address)
            loader.add_xpath('port', 'td[2]/text()')

            yield loader.load_item()