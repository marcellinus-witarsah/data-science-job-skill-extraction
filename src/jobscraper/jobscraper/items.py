# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobItem(scrapy.Item):
    job_title = scrapy.Field()
    job_listed = scrapy.Field()
    job_description = scrapy.Field()
    company_name = scrapy.Field()
    company_location = scrapy.Field()
    