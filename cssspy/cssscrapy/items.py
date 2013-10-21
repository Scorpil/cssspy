from scrapy.item import Item, Field
from cssspy.utils import CommonEqualityMixin

class CssFilesItem(Item, CommonEqualityMixin):
    page = Field()
    css_files = Field()
