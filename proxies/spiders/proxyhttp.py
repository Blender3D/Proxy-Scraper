import operator

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from proxies.items import Proxy, ProxyItemLoader

class ProxyhttpSpider(CrawlSpider):
    name = 'proxyhttp'
    allowed_domains = ['proxyhttp.net']
    start_urls = ['http://proxyhttp.net/']

    rules = (
        Rule(
            SgmlLinkExtractor(
                restrict_xpaths='//div[@id="pages"]',
                deny='/privatearea'
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def safe_eval(self, expression, variables):
        values = []

        for value in expression.split('^'):
            if value in variables:
                values.append(variables[value])
            else:
                values.append(int(value))

        return reduce(operator.xor, values)

    def get_variables(self, xpath):
        main_script = xpath.select('//script[contains(text(), "//<![CDATA[")][1]').select('text()').extract()[0]
        definitions = main_script.strip().splitlines()[1].strip().split(';')[:-1]
        variables = {}

        initial, value = definitions[0].split(' = ')
        variables[initial] = int(value)

        for definition in definitions[1:]:
            variable, value = definition.split(' = ')
            variables[variable] = self.safe_eval(value, variables)

        return variables

    def get_port(self, script, variables):
        expression = script.select('text()').re(r'document\.write\((.*?)\)')[0]

        return int(self.safe_eval(expression, variables))

    def parse_page(self, response):
        xpath = HtmlXPathSelector(response)
        variables = self.get_variables(xpath)

        for row in xpath.select('//table[@class="proxytbl"]/tr[position() > 1]'):
            loader = ProxyItemLoader(item=Proxy(), response=response, selector=row)

            if row.select('td[@class="t_https"]/text()').extract():
                loader.add_value('ssl', False)
            else:
                loader.add_value('ssl', True)
            
            loader.add_xpath('type', 'td[4]/text()')
            loader.add_value('port', self.get_port(row.select('td[@class="t_port"]/script'), variables))
            loader.add_xpath('address', 'td[@class="t_ip"]/text()')

            yield loader.load_item()