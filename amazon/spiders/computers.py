# -*- coding: utf-8 -*-
import scrapy

from amazon.items import AmazonItem

class ComputersSpider(scrapy.Spider):

    name = 'computers'
    allowed_domains = ["www.amazon.com"]
    #links:- 1: AIOs 2: mini pcs 3: tower pcs 4: 2 in 1 laptops 5: traditional laptops
    # start_urls = ['https://www.amazon.com/s/ref=lp_13896603011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565098%2Cn%3A13896603011&page=1&ie=UTF8&qid=1516656020',
    #               'https://www.amazon.com/s/ref=lp_13896591011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565098%2Cn%3A13896591011&page=1&ie=UTF8&qid=1516751032',
    #               'https://www.amazon.com/s/ref=lp_13896597011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565098%2Cn%3A13896597011&page=1&ie=UTF8&qid=1516752516',
    #               'https://www.amazon.com/s/ref=lp_13896609011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108%2Cn%3A13896609011&page=1&ie=UTF8&qid=1516752788',
    #               'https://www.amazon.com/s/ref=lp_13896615011_pg_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108%2Cn%3A13896615011&page=1&ie=UTF8&qid=1516753193']
    start_urls =['https://www.amazon.com/s/ref=lp_13896603011_pg_{}?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565098%2Cn%3A13896603011&page={}&ie=UTF8&qid=1516656020'.format(i,i)for i in range(2,6)]
    def parse(self, response):
        items={}
        asin = response.xpath('//li[@class="s-result-item celwidget  "]')
        for index, sel in enumerate(asin):
            items[index] = AmazonItem()  # instantiates items class
            id = sel.xpath('//li/@data-asin').extract()
            items[index]['product_id'] = ''.join(id[index]).strip()
            with open('log.txt', 'a') as f:
                f.write('https://www.amazon.com/product-reviews/{}/ref=cm_cr_getr_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&pageNumber='.format(items[index]['product_id']))
                f.write('\n')
        yield items
