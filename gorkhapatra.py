import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class gorkhapatra(scrapy.Spider):
    name="gorkhapatra"
    start_urls = ['https://gorkhapatraonline.com/']
    def __init__(self):
        self.f_gorkhapatra()
        self.news=[]

    def parse(self, response):
        main_div=response.xpath(self.main_div_xpath)[2]
        for article in main_div.xpath(self.article_xpath):

            title=article.xpath(self.title_xpath).get().replace('\n','').strip()
            link=article.xpath(self.link_xpath).attrib['href']
            print(title)
            print(link)
            
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        # main_section=response.xpath('//div[@class="col-lg-12"]')
        img_src=response.xpath(self.img_src_xpath).attrib['src']
        print(img_src)
        desc=response.xpath(self.description_xpath).xpath('string()').getall()
        description = ''.join(desc)
        print(description)
        date=response.xpath(self.date_xpath)[0].xpath('string()').get().strip()
        print(date)
        self.news.append({'title':title,'description':description,'date':date,'img_src':img_src,'link':link,'newspaper':'gorkhapatra' })
        print(self.news)

    def f_gorkhapatra(self):
        self.main_div_xpath='//div[@class="row"]'
        self.article_xpath='//div[@class="col-lg-12 mb-4"]'
        self.title_xpath='.//h2/a/text()'
        self.link_xpath='.//h2/a'
        self.main_section_xpath='//div[@class="col-lg-12"]'
        self.img_src_xpath='.//div[@class="blog-banner"]/img'
        self.description_xpath='//div[@class="blog-details"]/p'
        self.date_xpath='//span[@class="mr-3 font-size-16"]'

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_ENABLED': False,  
        'LOG_STDOUT': False,   
    })
process.crawl(gorkhapatra)
process.start()
# for n in news:
    # print(f'Title:{n["title"]}  date: {n["date"]} \nImage:{n["img_src"]} \nLink: {n["link"]} Newspaper:{n["newspaper"]}\nDescription: {n["description"]}')
