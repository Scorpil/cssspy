from urlparse import urlparse, urljoin


class CommonEqualityMixin(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

def domains_from_urls(*urls):
    """Retrieve domain names from urls."""
    return [urlparse(url).netloc for url in urls]

def absolute_urls(page, urls):
    """Construct absolute paths for relative ones."""
    return [urljoin(page, url) for url in urls]
