# -*- coding: utf-8 -*-
from amazon.items import AmazonItem
from scrapy.spiders import CrawlSpider
from scrapy import signals
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scrapy.http.request import Request

class review_reader(CrawlSpider):
    name = 'review_reader'
    allowed_domains = ["www.amazon.com"]
    start_urls = []#leave this blank as in our case we are going to read them from a file

    def start_requests(self):
        with open('log.txt', 'r') as f:
            for url in f.readlines():
                for i in range(1, 200):
                    new_url=(url.replace('\n','')+str(i))
                    self.log(new_url)
                    yield Request(new_url,self.parse)#trying to call first 200 paginations


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(review_reader, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_error, signal=signals.spider_error)#catches any error signal and any important info to pass to function spider_error
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)#cathes spider termination signal to call email notifier
        return spider

    def spider_error(self,failure,response,spider):
        spider.send_error_alert(self,failure,response,"Alert!!! an error occurred with the spider")#calls email function

    def spider_closed(self, spider):
        spider.send_mail("Crawling is complete. Thank you for using me :)", "Scraper Report")

    def send_error_alert(self,failure,response,title):
        self.log("Attempting to send email notification.")
        '''Note email addresses that uses gmail has to enable unsecure app connection in order for this to work'''
        gmailUser = ''#program's email address
        gmailPassword = ''#password
        recipient = ''#whoever

        message = str(failure) + str(response)
        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = title
        msg.attach(MIMEText(message))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        self.log("Mail sent")


    def send_mail(self, message, title):
        self.log("Attempting to send email notification.")
        '''Same as above'''
        gmailUser = ''
        gmailPassword = ''
        recipient = ''

        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = title
        msg.attach(MIMEText(message))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        self.log("Mail sent")


    def parse(self, response):
        items = {}
        reviews = response.xpath('//div[@data-hook="review"]')#gets a count of all items on the page
        # loop through sel times to add each comment
        for index, sel in enumerate(reviews):#enumerate because I need the index element and data for later use :)
            items[index] = AmazonItem()#instance of the items class (items.py)
            '''tries to find all text present in the stipulated paths and saves them to an item'''
            title = sel.xpath('//a[@data-hook ="review-title"]//text()').extract()
            author = sel.xpath('//a[contains(@data-hook, "review-author")]/text()').extract()
            rating = sel.xpath('//i[contains(@data-hook, "review-star-rating")]/span[contains(@class,"a-icon-alt")]/text()').extract()
            review_date = sel.xpath('//span[@data-hook="review-date"]//text()').extract()
            review_body = sel.xpath('//span[contains(@data-hook, "review-body")]').extract()

            '''Because the path selectors return a list we must iterate each record to add the database'''
            items[index]['customer_comments_title'] = ''.join(title[index]).strip()
            items[index]['customer_comments_author'] = ''.join(author[index]).strip()
            items[index]['customer_comments_date'] = ''.join(review_date[index]).strip('on')
            items[index]['customer_comments_rating'] = ''.join(rating[index]).replace('out of 5 stars', '')#removes text from rating
            items[index]['customer_comments_text'] = ''.join(review_body[index]).strip().replace('<br>', ' ').replace('<span data-hook="review-body" class="a-size-base review-text">', '').replace('</span>', '')
            yield items[index]  # returns everything in a record form for insertion


