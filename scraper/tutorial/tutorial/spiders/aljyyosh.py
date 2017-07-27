import scrapy
import unicodedata
from BeautifulSoup import BeautifulSoup



class AljyyoshSpider(scrapy.Spider):
	name = "alj"

	#start_urls = ['http://www.aljyyosh.org/archive.php']

	def start_requests(self):
		#url = 'http://www.aljyyosh.org/archive.php?page={0}'
		url = 'http://www.aljyyosh.org/onhold.php?page={0}'
		for page in range(5000):
		    yield scrapy.Request(url=url.format(page), callback=self.parse)

	def parse(self, response):	
		def extract_id(tag):
			#print(tag)
			href = tag.a['href']
			href = unicodedata.normalize('NFKD', href).encode('ascii','ignore')
			return href[href.find('=')+1:]

		rows = response.css('tr').extract()
		rows.pop()
		rows.pop()
		rows = rows[1:]
		rows = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in rows]
		rows = [x.replace('\n', '') for x in rows]
		rows = [x.replace('\t', '') for x in rows]
		parsed_rows = BeautifulSoup(''.join(rows))
		#res = [(extract_id(y[1]), extract_id(y[8])) for y in [x('td') for x in parsed_rows('tr')]]
		for x in parsed_rows('tr'):
			y = x('td')
			yield {
				'notifier' : extract_id(y[1]),
				'id' : extract_id(y[8]),
			}