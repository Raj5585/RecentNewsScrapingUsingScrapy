import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

news=[]
class AccessorySpider(scrapy.Spider):
    name="himalayan_times"
    start_urls = ['https://thehimalayantimes.com']


    def parse(self, response):
        main_div=response.xpath('//div[@class="row"]')[7]
        articles=main_div.xpath('.//div[@class="col-sm-6"]')
        for article in articles:
            link=article.xpath('.//a').attrib['href']
            yield scrapy.Request(url=link, callback=self.parse_article)


    def parse_article(self, response):
        article=response.xpath('//article[@class="articleDetails"]')
        title=article.xpath('//h1[@class="alith_post_title"]/text()').get().strip()

        article_date=article.xpath('//div[@class="article_date"]/text()').get()
        date_object = datetime.strptime(article_date, ' Published: %I:%M %p %b %d, %Y  ')
        formatted_date = date_object.strftime('%Y-%m-%d')

        desc=article.xpath('//div[@class="dropcap column-1 animate-box"]/p/text()').getall()

        img_src=article.xpath('//div[@class="articleImg"]/figure/div/picture/source').attrib['data-srcset']

        news.append({'title':title,'description':desc,'date':formatted_date,'img_src':img_src,'link':response.url,'newspaper':'The Himalayan Times' })
        

process = CrawlerProcess()
process.crawl(AccessorySpider)
process.start()
print(news)