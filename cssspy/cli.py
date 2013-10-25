import sys
import argparse
from . import __doc__
from . import __version__

from .utils import normalize_url, dead_selectors_report
from scrapy.log import level_names, INFO

__all__ = ('args',)


def get_args():
    parser = argparse.ArgumentParser(description=__doc__, prog='cssspy')

    # crawling arguments
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
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='list of urls of pages to start with')

    # logging arguments
    parser.add_argument('--loglevel', default=level_names[INFO].lower(),
                        choices=map(lambda s: s.lower(), level_names.values()),
                        help=('set the log verbosity level.\n' +
                              'Available choices: DEBUG, INFO, ' +
                              'WARNING, ERROR, CRITICAL or SILENT'))
    parser.add_argument('--logfile', default=None,
                        help="file to store the log")
    parser.add_argument('--stats', action='store_true', default=False,
                        help="show stats in the log after finish")
    parser.add_argument('--version', action='version',
                        version= __version__)

    args = parser.parse_args()

    # post-processing args
    args.urls = [normalize_url(url) for url in args.urls]
    if args.max_pages == 1:
        args.crawl = False
    args.loglevel = args.loglevel.upper()

    return args

def show_report(item, response, spider):
    sys.stdout.write(dead_selectors_report(item))

def show_error(error):
    print "Spider failed to complete the task: %s" % error.msg
