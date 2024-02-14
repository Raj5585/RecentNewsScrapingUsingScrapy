import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime


import logging
logging.getLogger().setLevel(logging.ERROR)
# Disable all logging messages (including Scrapy's) below WARNING level
logging.getLogger('scrapy').setLevel(logging.ERROR)
#news=[]

class Nagarik(scrapy.Spider):
    name="Nagarik"
    start_urls = ['https://nagarikpost.com/']
    scraped_items = []
    def __init__(self):
        self.article_xpath='//div[@class="maghny-grids-inf row mx-1"]/div'
        self.title_xpath='.//h2/a/text()'
        self.link_xpath='.//h2/a/'
        self.main_section_xpath='//div[@class=" bg-white"]'
        self.img_src_xpath='.//div[@class=" description "]/img'
        self.description_xpath='.//div[@class="desc"]/p/text()'
        self.date_xpath='//p[@class="text-muted font-italic"]/text()'

    def parse(self, response):
        print("Parsing")
        # articles=response.xpath(self.article_xpath).get()
        # print(articles)

        for article in response.xpath(self.article_xpath):
            # print(f"Article: {article.get()}")
            title=article.xpath(self.title_xpath).get()
            get_link=article.xpath(self.link_xpath).attrib['href']
            # link=f"https://myrepublica.nagariknetwork.com{get_link}"
            print(f"Title:{title}")
            print(f'Link: {get_link}')
            print()
            yield scrapy.Request(url=get_link, callback=self.parse_article,meta={'title':title,'link':get_link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath(self.main_section_xpath)
        
        img_src=main_section.xpath(self.img_src_xpath).attrib['src']
        print(f"Image:{img_src}")
        description=response.xpath(self.description_xpath).get()
        print(f"description:{description}")
        # desc=description.split(":")
        # print(f"Desc:{desc}")
        date=main_section.xpath(self.date_xpath).get().strip()
        print(f"Date:{date}")
        # index=date.find("NPT")
        # formatted_date=date[:index]
        news = {'title':title,'description':description,'date':date,'img_src':img_src,'link':link,'newspaper':'My Republica' }
        # print(news)
        self.scraped_items.append(news)
        return news
    
    def closed(self, reason):
        # Print or process items after the crawling process is complete
        print("Items after crawling:")
        for item in self.scraped_items:
            print(item)

# process = CrawlerProcess()
# process.crawl(Nagarik)

# process.start()
# print(news)

# def on_crawler_complete():
#     print("Crawling process completed!")

# process.signals.connect(on_crawler_complete, signal=process.signals.crawler_complete)