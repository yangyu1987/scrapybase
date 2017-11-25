# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy
from BaseTemp.items import ChaohaoItem
from BaseTemp.tools import header_list
from BaseTemp.utils.common import *


class LieSpider(scrapy.Spider):
    name = 'pianzi'
    allowed_domains = ['pianzi.com.cn']
    start_urls = ['http://www.pianzi.com.cn/shouji_1/']
    headers = header_list.get_header()

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'BaseTemp.pipelines.JsonPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
        },
        'MONGO_DB': 'swindler',
        'JOBDIR': 'info/pianzi/002',
        # 'LOG_FILE':'imdb_log.txt',
    }

    def parse(self, response):
        item = ChaohaoItem()
        temps = response.xpath('//ul[@class="news_list"]/li/a/@title').extract()
        for temp in temps:
            item['num'] = temp
            item['lables'] = '被举报电话'
            item['crawl_time'] = datetime.now().strftime('%Y-%m-%d')
            # item['mongo_collection'] = 'tel'
            yield item

        try:
            next_page = re.search('.*<a href="(.*?)">下一页</a>', response.text).group(1)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, headers=self.headers, callback=self.parse)

        except Exception as e:
            print('已经是最后一页')

    def parse_item(self, response):
        pass
