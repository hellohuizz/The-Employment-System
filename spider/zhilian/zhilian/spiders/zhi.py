# -*- coding: utf-8 -*-
import hashlib
import json

import scrapy
from zhilian.items import ZhilianItem

class ZhiSpider(scrapy.Spider):
    name = 'zhi'
    # allowed_domains = ['sou.zhaopin.com']
    citys = {'北京': 530, '上海': 538, '杭州': 653, '郑州': 719,'成都': 801,}
    keyword = input("请输入要查找的关键字：")
    city = input("请输入要查找的城市：")
    start_page = int(input('请输入起始页码-'))
    end_page = int(input('请输入结束页码-'))
    city_id = citys[city]
    start_urls = ['https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=60&cityId={}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'.format(city_id, keyword)]
    url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId={}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'
    def parse(self, response):
        content = json.loads(response.text)
        for i in content['data']['results']:
            # print(i)
            a = i['positionURL']
            update_time = i['updateDate']
            yield scrapy.Request(url=a,callback=self.content_parse,meta={'update_time': update_time, 'city': self.city})
        for page in range(self.start_page, self.end_page + 1):
            url = self.url.format((page-1) * 60, self.city_id, self.keyword)
            yield scrapy.Request(url=url,callback=self.parse)

    def content_parse(self,response):

        item = ZhilianItem()

        city_name = self.city

        jobname = response.xpath('//div[@class="main1 cl main1-stat"]/div/ul/li/h1/text()')[0].extract()

        salary = response.xpath('//div[@class="main1 cl main1-stat"]/div/ul/li/div/strong/text()')[0].extract()

        position = response.xpath('//div[@class="info-three l"]/span/a/text()')[0].extract()

        span = response.xpath('//div[@class="info-three l"]/span/text()').extract()
        if len(span) > 3:
            workingExp = span[1]
            eduLevel = span[2]
        else:
            workingExp = response.xpath('//div[@class="info-three l"]/span/text()')[0].extract()
            eduLevel = response.xpath('//div[@class="info-three l"]/span/text()')[1].extract()

        company_name = response.xpath('//div[@class="company l"]/a/text()')[0].extract()

        update_time = response.meta['update_time']

        require = response.xpath('//div[@class="pos-ul"]/p/text()').extract()
        if require == []:
            require = response.xpath('//div[@class="pos-ul"]/p/span/text()').extract()
        job_require = require
        sha1 = hashlib.sha1()
        string = (company_name + '' + update_time)
        stri = string.encode('utf8')
        sha1.update(stri)
        hash_id = sha1.hexdigest()

        for field in item.fields.keys():
            item[field] = eval(field)
        yield item
    import matplotlib