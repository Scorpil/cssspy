import sys
import lxml.html as lh
import urllib3

import tinycss
import cssselect

from cssspy.utils import absolute_urls


http = urllib3.PoolManager()


class CssspyScrapyPipeline(object):
    def process_item(self, item, spider):
        css_urls = absolute_urls(item['page_url'], item['css_links'])
        page_url = item['page_url']
        page_dom = lh.document_fromstring(item['page_body'])

        # TODO: multiprocessing? Hmmm... Maybe later.
        dead_selectors = []
        for css_url in css_urls:
            try:
                dead_selectors_on_page = self.process_css(page_dom, css_url)
            except cssselect.parser.SelectorSyntaxError:
                dead_selectors.append(None)
            else:
                dead_selectors.append(dead_selectors_on_page)

        report = self.create_report(page_url, css_urls, dead_selectors)
        sys.stdout.write(report)

    @staticmethod
    def create_report(page_url, css_urls, dead_selectors):
        double_line = '=' * 80 + '\n'
        line = '-' * 80 + '\n'
        report = ''

        report += double_line
        report += "PAGE: %s\n" % page_url

        for css_url, selectors in zip(css_urls, dead_selectors):
            report += 'CSS: %s\n' % css_url

            if selectors is None:
                report += line + "WARNING: couldn't parse file %s\n" % css_url
            elif len(selectors) == 0:
                report += 'No dead selectors\n'
            else:
                for selector in selectors:
                    report += selector + '\n'
            report += line + '\n'

        return report

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
