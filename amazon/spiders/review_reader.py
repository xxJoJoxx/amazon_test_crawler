# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from amazon.items import AmazonItem
from scrapy.http.request import Request

from pymongo import MongoClient

client = MongoClient()

class review_reader(CrawlSpider):
    name = 'review_reader'
    allowed_domains = ["www.amazon.com"]
    start_urls = []

    # to enable spider to read list of links from a text file
    # def __init__(self, filename=None):
    #     if filename:
    #         with open('log.txt', 'r') as f:
    #             self.start_urls = [url.strip() for url in f.readlines()]


    def start_requests(self):
        with open('log.txt', 'r') as f:
            for url in f.readlines():
                for i in range(1, 6):
                    new_url=(url.replace('\n','')+str(i))
                    self.log(new_url)
                    yield Request(new_url,self.parse)#trying to call first 5 paginations


    def parse(self, response):
        items = {}
        review_list = []
        # response = response.replace(body=response.body.replace('<br>', '\n'))
        reviews=response.xpath('//div[@data-hook="review"]')

        #loop through sel times to add each comment
        for index, sel in enumerate(reviews):
            items[index] = AmazonItem()
            title = sel.xpath('//a[@data-hook ="review-title"]//text()').extract()
            author = sel.xpath('//a[contains(@data-hook, "review-author")]/text()').extract()
            rating = sel.xpath('//i[contains(@data-hook, "review-star-rating")]/span[contains(@class,"a-icon-alt")]/text()').extract()
            review_date = sel.xpath('//span[@data-hook="review-date"]//text()').extract()
            review_body = sel.xpath('//span[contains(@data-hook, "review-body")]').extract()

            items[index]['customer_comments_title'] = ''.join(title[index]).strip()
            items[index]['customer_comments_author'] = ''.join(author[index]).strip()
            items[index]['customer_comments_date'] = ''.join(review_date[index]).strip('on')
            items[index]['customer_comments_rating'] = ''.join(rating[index]).replace('out of 5 stars','')
            # *** the important bit****
            items[index]['customer_comments_text'] = ''.join(review_body[index]).strip().replace('<br>',' ').replace('<span data-hook="review-body" class="a-size-base review-text">','').replace('</span>','')

            review_list.append(items[index])

        data = {
            'reviews': review_list
        }
        yield data

