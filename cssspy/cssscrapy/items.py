from scrapy.item import Item, Field


class CssFilesItem(Item):
    page_url = Field()
    page_body = Field()
    css_urls = Field()
    dead_selectors = Field()
