# -*- coding: utf-8 -*-
from amazon.items import AmazonItem
from scrapy.spiders import CrawlSpider
from scrapy import signals
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ComputersSpider(CrawlSpider):

    name = 'computers'
    allowed_domains = ["www.amazon.com"]
    #links:- 1: AIOs 2: mini pcs 3: tower pcs 4: 2 in 1 laptops 5: traditional laptops 6-8: tablets 9: fire tabs
    # start_urls = ['https://www.amazon.com/s/ref=lp_13896603011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565098%2Cn%3A13896603011&page=1&ie=UTF8&qid=1516656020',
    #               'https://www.amazon.com/s/ref=lp_13896591011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565098%2Cn%3A13896591011&page=1&ie=UTF8&qid=1516751032',
    #               'https://www.amazon.com/s/ref=lp_13896597011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565098%2Cn%3A13896597011&page=1&ie=UTF8&qid=1516752516',
    #               'https://www.amazon.com/s/ref=lp_13896609011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108%2Cn%3A13896609011&page=1&ie=UTF8&qid=1516752788',
    #               'https://www.amazon.com/s/ref=lp_13896615011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108%2Cn%3A13896615011&page=1&ie=UTF8&qid=1516753193',
    #               'https://www.amazon.com/s/ref=sr_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A1232597011%2Cp_n_operating_system_browse-bin%3A3077590011&page=1&ie=UTF8&qid=1516913821&lo=computers',
    #               'https://www.amazon.com/s/ref=sr_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A1232597011%2Cp_n_operating_system_browse-bin%3A3077591011&page=1&ie=UTF8&qid=1516913663&lo=computers',
    #               'https://www.amazon.com/s/ref=sr_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A1232597011%2Cp_n_operating_system_browse-bin%3A3077595011&page=1&ie=UTF8&qid=1516913665&lo=computers',
    #               'https://www.amazon.com/s/ref=lp_6669703011_pg_1?rh=n%3A16333372011%2Cn%3A%2116333373011%2Cn%3A2102313011%2Cn%3A6669703011&page=1&ie=UTF8&qid=1516914966']
    start_urls =['https://www.amazon.com/s/ref=sr_pg_{}?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A1232597011%2Cp_n_operating_system_browse-bin%3A3077595011&page={}&ie=UTF8&qid=1516917047&lo=computers'.format(i,i)for i in range(2,9)]


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ComputersSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.send_mail("Crawling is complete. Thank you for using me :)", "Scraper Report")

    def send_mail(self, message, title):
        self.log("Attempting to send email notification.")
        gmailUser = 'crawl.notify.group@gmail.com'
        gmailPassword = 'theworldshallknowtruepain'
        recipient = 'jklz521@gmail.com'

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
        asin = response.xpath('//li[@class="s-result-item s-result-card-for-container a-declarative celwidget  "]')
        for index, sel in enumerate(asin):
            items[index] = AmazonItem()  # instantiates items class
            id = sel.xpath('//li/@data-asin').extract()
            items[index]['product_id'] = ''.join(id[index]).strip()
            with open('log.txt', 'a') as f:
                f.write('https://www.amazon.com/product-reviews/{}/ref=cm_cr_getr_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&pageNumber='.format(items[index]['product_id']))
                f.write('\n')
        yield items
