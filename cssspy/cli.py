import sys
import argparse
from . import __doc__
from . import __version__

from .utils import normalize_url, dead_selectors_report

__all__ = ('args',)


def get_args():
    parser = argparse.ArgumentParser(description=__doc__, prog='cssspy')
    parser.add_argument('-c', '--crawl', action='store_true', default=False,
                        help="crawl linked pages.")
    parser.add_argument('-mp', '--max-pages', dest='max_pages', metavar='N',
                        type=int, default=100,
                        help=('maximal number of pages to crawl. ' +
                              'Only used with --crawl flag.'))
    parser.add_argument('-md', '--max-depth', dest='max_depth', metavar='N',
                        type=int, default=3,
                        help=('maximal depth of crawling. ' +
                              'Only used with --crawl flag.'))
    parser.add_argument('-t', '--timeout', metavar='S',
                        type=int, default=5*60,  # 5 minutes
                        help=('crawling timeout. ' +
                              'Only used with --crawl flag.'))
    parser.add_argument('--debug', action='store_true', default=False,
                        help='show debugging output.')
    parser.add_argument('--version', action='version',
                        version= __version__)
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='list of urls of pages to check')
    args = parser.parse_args()

    args.urls = [normalize_url(url) for url in args.urls]
    if args.max_pages == 1:
        args.crawl = False

    return args

def show_report(item, response, spider):
    sys.stdout.write(dead_selectors_report(item))

def show_error(error):
    print "Spider failed to complete the task: %s" % error.msg
