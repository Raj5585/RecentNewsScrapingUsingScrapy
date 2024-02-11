import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

news=[]

class annapurna(scrapy.Spider):
    name="annapurna"
    start_urls = ['https://www.annapurnapost.com/']

    def parse(self, response):
        for article in response.xpath('//div[@class="breaking__news"]'):
            title=article.xpath('.//h1/a/text()').get().replace('\n','').strip()
            get_link=article.xpath('.//h1/a').attrib['href']
            link=f"https://www.annapurnapost.com{get_link}"
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath('//div[@class="ap__news-content"]')
        img_src=main_section.xpath('.//div[@class="img__withSound noRiri"]/figure')
        print(img_src)
        description=response.xpath('//div[@class="news__details"]/p/text()').get()
        print(description)
        desc=description.split(":")[1]
        print(desc)
        date=main_section.xpath('//p[@class="date"]/span/text()').get()
        news.append({'title':title,'description':desc,'date':date,'img_src':img_src,'link':link,'newspaper':'Annapurna' })

process = CrawlerProcess()
process.crawl(annapurna)
process.start()
print(news)