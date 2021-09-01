import scrapy
from bs4 import BeautifulSoup
import requests

url = input("Enter your url:")
page = requests.get(url)
response_code = str(page.status_code)
if response_code=='200':
    val = 'valid url'
elif response_code=='404':
    val = 'invalid url'
data = page.text
soup = BeautifulSoup(data, features='lxml')

try:
    for link in soup.findAll('a'):

        print("Url:",link.get('href'),"| Status Code:",response_code, '| ',val)
except:
    for link in soup.findAll('a'):

        print("Url:",link.get('href'),"| Status Code:",response_code)



class wiki(scrapy.Spider):
    name = 'project'
    start_urls = ['https://en.wikipedia.org/wiki/Web_crawler']

    def parse(self, response ):
        title = response.css('#firstHeading::text').extract()
        info1 = response.css('p:nth-child(7)').extract()
        info2 = response.css('p:nth-child(8)').extract()
        references = response.css('#CITEREFSpetka .text:nth-child(1)').extract()
        yield {'title': title[0], 'content':BeautifulSoup(info1[0], features='lxml').text+BeautifulSoup(info2[0], features='lxml').text,'references': BeautifulSoup(references[0], features='lxml').text}
        next_page = response.css('h2+ ul li:nth-child(7) a::attr(href)').get()
        yield  response.follow(next_page, callback= self.parse_spider)


    def parse_spider(self,response):
        title = response.css('#firstHeading::text').extract()
        info = response.css('p:nth-child(4)').extract()
        references = response.css('#cite_note-2 .text').extract()
        yield {'title': title[0], 'content': BeautifulSoup(info[0], features='lxml').text,
               'references': BeautifulSoup(references[0],features='lxml').text}
        next_page = response.css('.div-col li:nth-child(4) a::attr(href)').get()
        yield response.follow(next_page, callback=self.parse_data)


    def parse_data(self,response):
        title = response.css('#firstHeading::text').extract()
        info = response.css('.searchaux+ p').extract()
        references = response.css('#cite_note-5 .text').extract()
        yield {'title': title[0], 'content': BeautifulSoup(info[0], features='lxml').text,
               'references': BeautifulSoup(references[0],features='lxml').text}