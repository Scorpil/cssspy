import sys
import lxml.html as lh
import urllib3

import tinycss
import cssselect

from cssspy.utils import absolute_urls
from scrapy import log


http = urllib3.PoolManager()


class CssspyScrapyPipeline(object):
    def process_item(self, item, spider):
        page_url = item['page_url']
        page_dom = lh.document_fromstring(item['page_body'])
        # TODO: multiprocessing? Hmmm... Maybe later.
        for css_url in item['css_urls']:
            try:
                dead_selectors_on_page = self.process_css(page_dom, css_url)
            except cssselect.parser.SelectorSyntaxError:
                item['dead_selectors'].append(None)
            else:
                item['dead_selectors'].append(dead_selectors_on_page)
        return item

    @classmethod
    def process_css(cls, page_dom, css_url):
        response = http.request('GET', css_url)
        if response.status != 200:
            raise cssselect.parser.SelectorSyntaxError()

        result = set()
        for selector_str_original in cls.selector_strings(response.data):
            selector_str = cls.remove_unsupported_classes(selector_str_original)
            if not selector_str:
                continue  # selector was just a pseudo-class

            add_to_results = None
            try:
                elements = page_dom.cssselect(selector_str)
            except cssselect.xpath.ExpressionError as e:
                add_to_results = False   # ignoring prefixes like -moz
            else:
                add_to_results = not bool(elements)

            if add_to_results:
                result.add(selector_str_original)
        return result

    # Utils
    @staticmethod
    def selector_strings(css_file):
        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet(css_file)
        for rule in stylesheet.rules:
            if rule.at_keyword is None:  # skip @-rules
                yield rule.selector.as_css()

    @staticmethod
    def remove_unsupported_classes(selector_str):
        unsupported_classes = (':hover', ':active', ':focus',
                               ':target', ':visited', ':link',
                               ':enabled', ':disabled', ':checked')
        for css_class in unsupported_classes:
            selector_str = selector_str.replace(css_class, '')
        return selector_str.rstrip(', ')
