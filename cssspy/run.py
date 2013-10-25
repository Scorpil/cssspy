import os
from .cli import get_args, show_report, show_error

from twisted.internet import reactor
from scrapy import signals, log
from scrapy.crawler import Crawler
from scrapy.settings import CrawlerSettings
from scrapy.utils.project import get_project_settings

from . import ExitStatus
from .cssscrapy.spiders import CssCrawlSpider, CssBaseSpider
from .cssscrapy import settings as settings_module


def run():
    args = get_args()
    spider = get_spider(args.crawl)(urls=args.urls)
    run_crawler(spider, args_to_settings(args))
    reactor.run()
    os._exit(ExitStatus.OK)

def handle_error(failure, response, spider):
    show_error(failure.value)
    os._exit(ExitStatus.ERROR)

def run_crawler(spider, settings):
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.signals.connect(show_report, signal=signals.item_scraped)
    crawler.signals.connect(handle_error, signal=signals.spider_error)
    crawler.configure()
    crawler.crawl(spider)
    if settings['LOG_ENABLED']:
        log.start_from_settings(settings, crawler=crawler)
    crawler.start()

def args_to_settings(args):
    settings = CrawlerSettings(settings_module)
    settings.overrides['LOG_LEVEL'] = args.loglevel
    settings.overrides['LOG_FILE'] = args.logfile
    settings.overrides['STATS_DUMP'] = args.stats
    settings.overrides['DEPTH_LIMIT'] = args.max_depth
    settings.overrides['CLOSESPIDER_ITEMCOUNT'] = args.max_pages
    settings.overrides['CLOSESPIDER_TIMEOUT'] = args.timeout
    return settings

def get_spider(crawl):
    if crawl:
        return CssCrawlSpider
    else:
        return CssBaseSpider
