import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class himalayan_times(scrapy.Spider):
    name="himalayan_times"
    start_urls = ['https://thehimalayantimes.com']

    def __init__(self):
        self.himalayan()
        self.news=[]

    def parse(self, response):
        main_div=response.xpath(self.main_div_xpath)[7]
        articles=main_div.xpath(self.article_xpath)
        for article in articles:
            link=article.xpath(self.link_xpath).attrib['href']
            yield scrapy.Request(url=link, callback=self.parse_article)


    def parse_article(self, response):
        main_section=response.xpath(self.main_section_xpath)
        title=main_section.xpath(self.title_xpath).get().strip()

        article_date=main_section.xpath(self.date_xpath).get()
        date_object = datetime.strptime(article_date, ' Published: %I:%M %p %b %d, %Y  ')
        formatted_date = date_object.strftime('%Y-%m-%d')

        desc=main_section.xpath(self.description_xpath).getall()
        description = ''.join(desc)

        img_src=main_section.xpath(self.img_src_xpath).attrib['data-srcset']

        self.news.append({'title':title,'description':description,'date':formatted_date,'img_src':img_src,'link':response.url,'newspaper':'The Himalayan Times' })
        print(self.news)

    def himalayan(self):
        self.main_div_xpath='//div[@class="row"]'
        self.article_xpath='.//div[@class="col-sm-6"]'
        self.link_xpath='.//a'
        self.main_section_xpath='//article[@class="articleDetails"]'
        self.title_xpath='//h1[@class="alith_post_title"]/text()'
        self.img_src_xpath='//div[@class="articleImg"]/figure/div/picture/source'
        self.description_xpath='//div[@class="dropcap column-1 animate-box"]/p/text()'
        self.date_xpath='//div[@class="article_date"]/text()'



process = CrawlerProcess()
process.crawl(himalayan_times)
process.start()