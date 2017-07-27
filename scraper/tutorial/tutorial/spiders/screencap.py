import scrapy
import unicodedata
import os
from BeautifulSoup import BeautifulSoup
from tutorial.items import Listing



class ScreencapSpider(scrapy.Spider):
	name = "screencap"

	#start_urls = ['http://www.aljyyosh.org/archive.php']

	def start_requests(self):
		f = open("onhold_sifted.txt", 'r')
		url = 'http://www.aljyyosh.org/show_mirror.php?id='
		for line in f:
		    yield scrapy.Request(url=url+line, callback=self.parse)

	def parse(self, response):
		item = Listing()
		item['url'] = response.url
		item['html'] = response.body
		yield item