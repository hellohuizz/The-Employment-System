# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataProItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    place = scrapy.Field()
    experience = scrapy.Field()
    Education = scrapy.Field()
    company = scrapy.Field()
    push_time = scrapy.Field()
    hash_id = scrapy.Field()
    item_meta = scrapy.Field()
    job_requirements=scrapy.Field()
