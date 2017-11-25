# -*- coding: utf-8 -*-
import re
from datetime import datetime

import scrapy

from BaseTemp.items import ChaohaoItem
from BaseTemp.tools import header_list
from BaseTemp.utils.common import *


class ChahaoSpider(scrapy.Spider):
    name = 'chahao'
    allowed_domains = ['chahaoba.com']
    start_urls = ['https://www.chahaoba.com/分类:骗子号码']

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY' : 1,
        'ITEM_PIPELINES': {
            'BaseTemp.pipelines.MongoPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
        },
        'MONGO_DB': 'swindler',
        'JOBDIR': 'info/chahaoba/001',
        # 'LOG_FILE':'imdb_log.txt',
    }
    headers = header_list.get_header()

    def parse(self, response):
        item = ChaohaoItem()
        temps = response.xpath('//div[@class="mw-category"]//li')
        print(temps)
        for temp in temps:
            nums = temp.xpath('a/text()').extract()[0]
            num = get_all_num(nums)
            item['num'] = num
            item['lables'] = '诈骗'
            item['crawl_time'] = datetime.now().strftime('%Y-%m-%d')
            item['mongo_collection'] = 'tel'
            yield item

        try:
            next_page = re.search('.*<a href="(.*?)" title=".*?">下一页</a>',response.text).group(1)
            next_page = response.urljoin(next_page.replace('amp;', '').replace('amp', ''))
            yield scrapy.Request(next_page,headers=self.headers,callback=self.parse)

        except Exception as e:
            print('已经是最后一页')

