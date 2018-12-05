# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    jobname = scrapy.Field() # 职位名称
    position = scrapy.Field() # 位置
    workingExp = scrapy.Field() # 工作经验
    eduLevel = scrapy.Field() # 学历
    salary = scrapy.Field() # 工资
    company_name = scrapy.Field()
    update_time = scrapy.Field()
    job_require = scrapy.Field()
    hash_id = scrapy.Field()