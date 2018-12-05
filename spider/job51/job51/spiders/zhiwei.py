# -*- coding: utf-8 -*-
import hashlib

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from job51.items import Job51Item

class ZhiweiSpider(CrawlSpider):
    name = 'zhiwei'
    # allowed_domains = ['search.51job.com']
    citys = {'北京': '010000', '上海': '020000', '杭州': '080200', '郑州': '170200','成都': '090200',}
    position = input("请输入职位关键字：")
    city = input("请输入城市：")
    city_id = citys[city]
    start_urls = ['https://search.51job.com/list/{},000000,0000,00,9,99,{},2,1.html?lang=c'.format(city_id,position)]

    content_link = LinkExtractor(restrict_xpaths='//div[@id="resultList"]/div/p/span/a')
    page_link = LinkExtractor(restrict_xpaths='//div[@class="p_in"]/ul/li/a')

    rules = (
        Rule(content_link, callback='parse_item', follow=False),
        Rule(page_link,follow=True)
    )
    str = ''
    def parse_item(self, response):

        item =  Job51Item()

        city_name = self.city
        jobname =  response.xpath('//div[@class="cn"]/h1/@title')[0].extract()
        position = response.xpath('//div[@class="cn"]/p/@title')[0].extract().split('|')[0].strip('\xa0\xa0')
        workingExp = response.xpath('//div[@class="cn"]/p/@title')[0].extract().split('|')[1].strip('\xa0\xa0')
        eduLevel = response.xpath('//div[@class="cn"]/p/@title')[0].extract().split('|')[2].strip('\xa0\xa0')
        salary = response.xpath('//div[@class="cn"]/strong/text()')[0].extract()
        company_name = response.xpath('//div[@class="cn"]/p/a/@title')[0].extract()
        update_time = response.xpath('//div[@class="cn"]/p/@title')[0].extract().split('|')[4].strip('\xa0\xa0')
        require = response.xpath('//div[@class="bmsg job_msg inbox"]/p/text()').extract()
        for i in require:
            self.str += i[2:]
        job_require = self.str

        sha1 = hashlib.sha1()
        string = (company_name + '' + update_time)
        stri = string.encode('utf8')
        sha1.update(stri)
        hash_id = sha1.hexdigest()

        for field in item.fields.keys():
            item[field] = eval(field)
        yield item
