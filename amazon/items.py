# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_id = scrapy.Field()
    product_rating = scrapy.Field()
    product_link = scrapy.Field()
    customer_comments_text = scrapy.Field()
    customer_comments_author = scrapy.Field()
    customer_comments_title = scrapy.Field()
    customer_comments_date = scrapy.Field()
    customer_comments_rating = scrapy.Field()
    customer_comments_helpful_count = scrapy.Field()
    # striped_review_count = scrapy.Field()