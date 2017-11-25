# -*- coding: utf-8 -*-
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from BaseTemp.items import HcUrlItem
from BaseTemp.tools import header_list
import time


class Hc360cSpider(CrawlSpider):
    name = 'hc360c'
    allowed_domains = ['hc360.com']
    start_urls = ['https://js.hc360.com/category/cn.html']
    headers = header_list.get_header()

    rules = (
        Rule(LinkExtractor(allow=r'cn/.*?/$',deny=r'.*?cn/.*?/company-.*'), follow=True, callback='parse_area'),
        Rule(LinkExtractor(allow=r'cn/.*?/\d+/$',deny=r'.*?cn/.*?/company-.*'), follow=True, callback='parse_area'),
        # Rule(),
    )
    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        # 'DOWNLOAD_DELAY': 0.3,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
        'RETRY_TIMES': 1000,
        'ITEM_PIPELINES': {
            'BaseTemp.pipelines.MongoPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
            #'BaseTemp.middlewares.ProxyMiddleware': 10,
        },
        'MONGO_DB': 'hc360',
        # 'JOBDIR': 'info/hc360/002',
    }

    def parse_area(self, response):
        # 解析构造本地企业url
        item = HcUrlItem()
        comp_url = response.xpath('//article/ul/li/div')
        for url in comp_url:
            item['crawl_time'] = datetime.now().strftime('%Y-%m-%d')
            item['comp_name'] = url.xpath('a/text()').extract()[0]
            url_temp = url.xpath('a/@href').extract()[0]
            item['comp_id'] = re.search('/company-(.*?)/',url_temp).group(1)
            item['comp_page'] = item['comp_id'] + '.b2b.hc360.com/shop/company.html'
            item['mongo_collection'] = 'url'
            yield item

    # def parse_detail(self,response):
    #     print(response.text)
    #     pass