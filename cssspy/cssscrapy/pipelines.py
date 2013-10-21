import os
import json
from cssspy.utils import absolute_urls


class CssspyScrapyPipeline(object):
    def process_item(self, item, spider):
        json.dumps(item)
        return item
