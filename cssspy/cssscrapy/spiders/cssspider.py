from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from cssspy.utils import domains_from_urls, absolute_urls
from cssspy.cssscrapy.items import CssFilesItem
from scrapy.contrib.linkextractors.htmlparser import HtmlParserLinkExtractor



class CssSpiderMixin(object):
    name = "css"
    def __init__(self, urls=None, *args, **kwargs):
        self.start_urls = urls
        self.allowed_domains = domains_from_urls(*self.start_urls)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        css_links = hxs.select('//link[@rel="stylesheet"]/@href').extract()
        item = CssFilesItem()
        item['page_url'] = response.url
        item['page_body'] = response.body
        item['css_urls'] = absolute_urls(response.url, css_links)
        item['dead_selectors'] = []
        return item


class CssCrawlSpider(CssSpiderMixin, CrawlSpider):

    rules = (
        Rule(HtmlParserLinkExtractor(), callback='parse_item', follow=True
         ),
    )

    def __init__(self, *args, **kwargs):
        CrawlSpider.__init__(self, *args, **kwargs)
        CssSpiderMixin.__init__(self, *args, **kwargs)

class CssBaseSpider(CssSpiderMixin, BaseSpider):

    def __init__(self, *args, **kwargs):
        BaseSpider.__init__(self, *args, **kwargs)
        CssSpiderMixin.__init__(self, *args, **kwargs)

    def parse(self, response):
        return self.parse_item(response)
