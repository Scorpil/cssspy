from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from cssspy.utils import domains_from_urls
from cssspy.cssscrapy.items import CssFilesItem


class CssSpider(CrawlSpider):
    name = "css"

    rules = (
        Rule(SgmlLinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def __init__(self, urls=None, *args, **kwargs):
        super(CssSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(' ')
        self.allowed_domains = domains_from_urls(*self.start_urls)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        css_links = hxs.select('//link[@rel="stylesheet"]/@href').extract()
        item = CssFilesItem()
        item['page_url'] = response.url
        item['page_body'] = response.body
        item['css_links'] = css_links
        return item
