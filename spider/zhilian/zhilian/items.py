# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    jobname = scrapy.Field()
    salary = scrapy.Field()
    position = scrapy.Field()
    workingExp = scrapy.Field()
    eduLevel = scrapy.Field()
    update_time = scrapy.Field()
    company_name = scrapy.Field()
    job_require = scrapy.Field()
    hash_id = scrapy.Field()