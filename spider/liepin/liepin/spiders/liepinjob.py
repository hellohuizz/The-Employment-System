# -*- coding: utf-8 -*-
import hashlib

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from liepin.items import LiepinItem

class LiepinjobSpider(CrawlSpider):
    name = 'liepinjob'
    allowed_domains = ['www.liepin.com']
    keyword = input("请输入职位关键字：")
    city = input("请输入城市：")
    citys = {'北京': '010', '上海': '020', '杭州': '070020', '郑州': '150020', '成都': '280020',}
    city_id = citys[city]
    start_urls = ['https://www.liepin.com/zhaopin/?isAnalysis=&init=-1&searchType=1&headckid=5fd0af40862640e3&flushckid=1&dqs={}&pubTime=&compkind=&fromSearchBtn=2&salary=&sortFlag=15&ckid=694535710b437fd0&industryType=&jobKind=&industries=&compscale=&clean_condition=&key={}&siTag=I-7rQ0e90mv8a37po7dV3Q~-Gw6taVFUG4CWqViHEM79A&d_sfrom=search_prime&d_ckId=1604ebc816f751e9f23f1077cf967e30&d_curPage=0&d_pageSize=40&d_headId=48450588b70f855415a88f3f2bf8c288'.format(city_id, keyword)]
    content_link = LinkExtractor(restrict_xpaths='//div[@class="sojob-result "]/ul/li/div//h3/a')
    page_link = LinkExtractor(restrict_xpaths='//div[@class="pagerbar"]/a')
    l = 0
    rules = (
        Rule(content_link, callback='parse_item', follow=False),
        Rule(page_link,follow=True)
    )

    def parse_item(self, response):

        item = LiepinItem()

        city_name = self.city
        jobname1 = response.xpath('//div[@class="title-info"]/h1/text()')
        if jobname1 == []:
            jobname = response.xpath('//div[@class="title-info "]/h1/text()')[0].extract()
        else:
            jobname = jobname1[0].extract()
        span = response.xpath('//p[@class="basic-infor"]/span/a/text()').extract()
        if span == []:
            position = response.xpath('//p[@class="basic-infor"]/span/text()')[0].extract()
        else:
            position = span[0]
        workingExp = response.xpath('//div[@class="job-qualifications"]/span/text()')[1].extract()
        eduLevel = response.xpath('//div[@class="job-qualifications"]/span/text()')[0].extract()
        salary = response.xpath('//div[@class="job-title-left"]/p/text()')[0].extract().rstrip('\r\n ')
        company_name = response.xpath('//div[@class="title-info"]/h3/a/text()')[0].extract()
        update_time = response.xpath('//p[@class="basic-infor"]/time/@title')[0].extract()
        job_require = response.xpath('//div[@class="content content-word"]/text()').extract()

        sha1 = hashlib.sha1()
        string = (company_name + '' + update_time)
        stri = string.encode('utf8')
        sha1.update(stri)
        hash_id = sha1.hexdigest()

        for field in item.fields.keys():
            item[field] = eval(field)
        yield item
