import inspect
from urlparse import urlparse, urljoin


def domains_from_urls(*urls):
    """Retrieve domain names from urls."""
    return [urlparse(url).hostname for url in urls]

def absolute_urls(page, urls):
    """Construct absolute paths for relative ones."""
    return [urljoin(page, url) for url in urls]
