# -*- coding: utf-8 -*-
import datetime
import hashlib
import time

import requests

import scrapy
from lxml import etree
from scrapy import Request
from data_pro.items import DataProItem


class GetDataSpider(scrapy.Spider):
    name = 'get_data'
    allowed_domains = ['www.zhipin.com']

    def start_requests(self):
        self.page = 1
        print('您当前可选的城市有:北京,杭州,上海,武汉,广州,深圳')
        self.query = input('要查询的职位: ')
        self.scity = input('城市: ')
        page = 1
        self.dic = {'北京': '101010100', '杭州': '101210100', '上海': '101020100', '武汉': '101200100', '广州': '101280100',
                    '深圳': '101280600'}
        self.start_urls = 'https://www.zhipin.com/job_detail/?query={}&scity={}&industry=&position='.format(self.query,
                                                                                                            self.dic.get(
                                                                                                                self.scity))

        yield Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        resp = response.xpath('//*[@id="main"]/div/div[3]/ul/li/div/div[1]/h3/a/@href').extract()

        for res in resp:
            a_href = 'https://www.zhipin.com' + res
            yield Request(url=a_href, callback=self.parse_info)
        if self.page < 10:
            self.page += 1
            # print('this is 循环:::  ', self.page)
            url = 'https://www.zhipin.com/c{}/?query={}&page={}&ka=page-{}'.format(self.dic.get(self.scity),
                                                                                   self.query,
                                                                                   self.page, self.page)
            # print('this is 循环:::  ', url)
            yield Request(url=url, callback=self.parse)

    # # 解析函数
    def parse_info(self, response):
        print('=' * 50)
        item = DataProItem()
        # # 职位
        name = response.xpath('//div[@class="info-primary"]/div[@class="name"]/h1/text()').extract()[0]
        item['name'] = name
        # 薪资
        salary = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()').extract()[0].replace('\n',
                                                                                                                 '').strip()
        item['salary'] = salary
        # 地点
        result = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()').extract()
        place = result[0]
        item['place'] = place
        # # 经验
        experience = result[1]
        item['experience'] = experience
        # 学历
        Education = result[2]
        item['Education'] = Education
        # # 公司
        company = response.xpath('//*[@id="main"]/div[1]/div/div/div[3]/h3/a/text()')[0].extract()
        item['company'] = company
        # 发布时间
        push_time = response.xpath('//span[@class="time"]/text()')[0].extract()
        item['push_time'] = push_time
        # 任职要求
        job_requirements = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div/text()').extract()
        job_requirement = ''
        for i in job_requirements:
            job_requirement += i.replace('\u2028', '').strip('\xe5').strip()

        item['job_requirements'] = job_requirement
        # 根据上传字段生成hash值
        sha1 = hashlib.sha1()
        string = str(company + push_time + name + Education + experience + place + salary + job_requirement)
        stri = string.encode('utf8')
        sha1.update(stri)
        item['hash_id'] = sha1.hexdigest()
        item['item_meta'] = self.scity  # 参数
        time.sleep(1)
        yield item
        print('=' * 50)
