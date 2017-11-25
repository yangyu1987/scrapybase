# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from BaseTemp.items import BasetempItem
from BaseTemp.tools import header_list
from scrapy import log


class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['test.com']
    start_urls = ['https://www.douban.com/']

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        # 'DOWNLOAD_DELAY': 1,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
        'RETRY_TIMES': 100,
        # 'ITEM_PIPELINES': {
        #     'BaseTemp.pipelines.ImdbMongoPipeline': 300,
        # },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
            # 'BaseTemp.middlewares.ProxyMiddleware': 10,
        },
        # 'MONGO_DB': 'hc360',
        # 'JOBDIR': 'info/hc360/002',
    }
    headers = header_list.get_header()

    def parse(self, response):
        # log.msg("This is a warning", level=log.WARNING)
        log.WARNING
        print(response.status)
