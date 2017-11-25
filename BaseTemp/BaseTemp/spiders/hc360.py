# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy
from BaseTemp.items import HcUrlItem
from BaseTemp.tools import header_list


class Hc360Spider(scrapy.Spider):
    name = 'hc360'
    allowed_domains = ['hc360.com']
    start_urls = ['https://js.hc360.com/category/cn.html']
    headers = header_list.get_header()

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
        'RETRY_TIMES': 1000,
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {
            'BaseTemp.pipelines.MongoPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
            # 'BaseTemp.middlewares.ProxyMiddleware': 10,
        },
        'MONGO_DB': 'hc360',
        # 'JOBDIR': 'info/hc360/002',
    }

    def parse(self, response):
        area_url = response.xpath('//article/ul/li/a/@href').extract()
        # area_url = ['https://js.hc360.com/cn/sh/']
        for url in area_url:
            yield scrapy.Request(url=response.urljoin(url),headers=self.headers,callback=self.pares_page_num)

    def pares_page_num(self,response):
        # 第一次请求时截获全部页面数，用于下面直接发请求
        # 使用自动寻找是系统会直接ban掉下一页的链接
        nums = re.search('共(.*)页',response.text).group(1)
        page_num = int(nums.strip())
        for num in range(2,page_num):
            page_url = response.url+str(num)+'/'
            yield scrapy.Request(url=page_url, headers=self.headers, callback=self.parse_area)

    def parse_area(self, response):
        # 解析构造本地企业url
        item = HcUrlItem()
        comp_url = response.xpath('//article/ul/li/div')
        for url in comp_url:
            item['crawl_time'] = datetime.now().strftime('%Y-%m-%d')
            item['comp_name'] = url.xpath('a/text()').extract()[0]
            url_temp = url.xpath('a/@href').extract()[0]
            item['comp_id'] = re.search('/company-(.*?)/',url_temp).group(1)
            item['comp_page'] = item['comp_id'] + 'b2b.hc360.com/shop/company.html'
            item['mongo_collection'] = 'url'
            yield item

        # try:
        #     next_page = response.xpath('//a[@class="page-next"]/@href').extract()[0]
        #     yield scrapy.Request(url=response.urljoin(next_page),headers=self.headers,callback=self.parse_area)
        #     # yield scrapy.Request(url=comp_detail_url,headers=self.headers,callback=self.parse_detail)
        # except:
        #     print('已爬取完毕')

    # def parse_detail(self,response):
    #     print(response.text)
    #     pass