import inspect
from urlparse import urlparse, urlunparse, urljoin


def domains_from_urls(*urls):
    """Retrieve domain names from list of urls."""
    return [urlparse(url).hostname for url in urls]

def absolute_urls(page, urls):
    """Construct absolute paths from list of links."""
    return [urljoin(page, url) for url in urls]

def normalize_url(url):
    """Transform url to canonical form."""
    if '://' not in url:
        url = "http://%s" % url
    parsed = urlparse(url.lower())
    return urlunparse(parsed)

def dead_selectors_report(item):
    double_line = '=' * 80 + '\n'
    line = '-' * 80 + '\n'
    report = ''

    report += double_line
    report += "PAGE: %s\n" % item['page_url']

    for css_url, selectors in zip(item['css_urls'], item['dead_selectors']):
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
