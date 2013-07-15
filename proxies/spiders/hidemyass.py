import cssutils

from bs4 import BeautifulSoup
from bs4.element import NavigableString

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from proxies.items import Proxy, ProxyItemLoader

FORM_DATA = {
    'ac': 'on',
    'p': '',
    'pr[]': ['0', '1', '2'],
    'a[]': ['0', '1', '2', '3', '4'],
    'sp[]': ['1', '2', '3'],
    'ct[]': ['1', '2', '3'],
    's': '0',
    'o': '0',
    'pp': '3'
}

class HidemyassSpider(CrawlSpider):
    name = 'hidemyass'
    allowed_domains = ['hidemyass.com']
    start_url = 'http://hidemyass.com/proxy-list/'

    rules = (
        Rule(
            SgmlLinkExtractor(
                restrict_xpaths='//div[@id="pagination"]'
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def start_requests(self):
        yield Request(
            url=self.start_url,
            dont_filter=True,
            callback=self.search
        )

    def search(self, response):
        yield FormRequest.from_response(
            response=response,
            callback=self.parse_page,
            formdata=FORM_DATA
        )

    def get_ip(self, parent):
        soup = BeautifulSoup(parent.extract()[0])
        
        displayed_text = ''
        css = cssutils.parseString(soup.find('style').get_text())

        display_mapping = {
            rule.selectorText[1:]: rule.style.display != 'none' for rule in css.cssRules
        }

        for element in soup.find('style').next_siblings:
            if isinstance(element, NavigableString):
                displayed_text += str(element)
                continue

            if 'none' in element.get('style', ''):
                continue

            class_name = element.get('class')

            if class_name and not display_mapping.get(class_name[0], True):
                continue

            displayed_text += element.get_text()

        return displayed_text

    def parse_page(self, response):
        xpath = HtmlXPathSelector(response)

        for row in xpath.select('//table[@id="listtable"]/tr'):
            loader = ProxyItemLoader(item=Proxy(), response=response, selector=row)

            loader.add_xpath('port', 'td[3]/text()')
            loader.add_xpath('type', 'td[7]/text()')
            loader.add_value('address', self.get_ip(row.select('td[2]/span')))

            yield loader.load_item()

        for request in self.parse(response):
            yield request