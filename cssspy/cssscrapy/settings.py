BOT_NAME = 'csssscrapy'

SPIDER_MODULES = ['cssspy.cssscrapy.spiders']
NEWSPIDER_MODULE = 'cssspy.cssscrapy.spiders'

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False

ITEM_PIPELINES = {
    'cssspy.cssscrapy.pipelines.CssspyScrapyPipeline': 100,
}

#USER_AGENT = 'cssspy_scrapy (+http://www.yourdomain.com)'
