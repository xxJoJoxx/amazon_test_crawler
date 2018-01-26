# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class AmazonPipeline(object):
    def open_spider(self, spider):
        hostname = ''#your host
        username = ''#your username
        password = ''#your password
        database = ''#database name
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into review_data_raw(customer_comments_title,customer_comments_author,customer_comments_date,customer_comments_rating,customer_comments_text) values(%s,%s,%s,%s,%s)",
                         (item['customer_comments_title'], item['customer_comments_author'], item['customer_comments_date'], item['customer_comments_rating'],item['customer_comments_text']))
        self.connection.commit()
        return item
