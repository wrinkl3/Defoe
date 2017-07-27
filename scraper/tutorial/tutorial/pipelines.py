# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import hashlib

class HtmlFilePipeline(object):
    def process_item(self, item, spider):
        file_name = hashlib.sha224(item['url']).hexdigest() #chose whatever hashing func works for you
        with open('files/%s.html' % file_name, 'w+b') as f:
            f.write(item['html'])