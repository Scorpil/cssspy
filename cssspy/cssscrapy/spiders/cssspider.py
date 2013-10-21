from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from cssspy.utils import domains_from_urls
from cssspy.cssscrapy.items import CssFilesItem


class CssSpider(BaseSpider):
    name = "css"

    def __init__(self, urls=None, *args, **kwargs):
        super(CssSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(' ')
        self.allowed_domains = domains_from_urls(*self.start_urls)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        css_files = hxs.select('//link[@rel="stylesheet"]/@href').extract()
        item = CssFilesItem()
        item['page'] = response.url
        item['css_files'] = css_files
        return item
