import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime


import logging
logging.getLogger().setLevel(logging.ERROR)
# Disable all logging messages (including Scrapy's) below WARNING level
logging.getLogger('scrapy').setLevel(logging.ERROR)
#news=[]

class Bbc(scrapy.Spider):
    name="bbc"
    start_urls = ['https://www.bbc.com/nepali']
    scraped_items = []
    def __init__(self):
        # //div[contains(@class, 'gel-layout__item') and contains(@class, 'nw-c-top-stories__secondary-item')]
        self.articles_section_xpath="//div[@data-testid='hierarchical-grid']/ul"
        self.article_xpath='.//li'
        self.title_xpath='.//div/div[@class="promo-text"]/h3/a/text()'
        self.alternate_title_xpath='.//div/div[@class="promo-text"]/h3/a/span/text()'
        self.link_xpath='.//div/div[@class="promo-text"]/h3/a'
        self.main_section_xpath='//main'
        self.img_src_xpath='.//figure/div/picture/img/@src'
        self.alternate_img_src_xpath='.//div/div/figure/div/div/img/@src'
        self.description_xpath='.//div[@dir="ltr"]/p'
        self.date_xpath='.//div/time/@datetime'

    def parse(self, response):
        print("Parsing")
        # articles=response.xpath(self.article_xpath).get()
        # print(articles)

        articles=response.xpath(self.articles_section_xpath)[0]
        count=0
        for article in articles.xpath(self.article_xpath):
            count+=1
            # print(f"Article: {article.get()}")
            title=article.xpath(self.title_xpath).get()
            if title is None:
                title=article.xpath(self.alternate_title_xpath).get()
            link=article.xpath(self.link_xpath).attrib['href']
            # print(f"{count}:Title:{title}")
            # print(f'{count}:Link: {link}')
            # print()
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath(self.main_section_xpath)
        
        img_src=main_section.xpath(self.img_src_xpath).get()
        if img_src is None:
            img_src=main_section.xpath(self.alternate_img_src_xpath).get()
        # print(f"Image:{img_src}")
        description_elements=main_section.xpath(self.description_xpath)
        description=""
        for item in description_elements:
            # print(f"Item:{item.get()}")
            description = description + item.xpath('.//text()').get()+"\n"
            if len(description.split())>60:
                description=description.strip()
                break
            # if description is not None:
            #     break
        # print(f"description:{description}")
        date=main_section.xpath(self.date_xpath).get().strip()
        # print(f"Date:{date}")
   
        news = {'title':title,'description':description,'date':date,'img_src':img_src,'link':link,'newspaper':'BBC News' }
        # # print(news)
        self.scraped_items.append(news)
        # return news
    
    def closed(self, reason):
        # Print or process items after the crawling process is complete
        print("Items after crawling:")
        for item in self.scraped_items:
            print(f"Title:{item['title']}\nLink:{item['link']}\nDescription:{item['description']}\nImage:{item['img_src']}\nNewspaper:{item['newspaper']}\tDate:{item['date']}\n\n")

# process = CrawlerProcess()
# process.crawl(Nagarik)

# process.start()
# print(news)

# def on_crawler_complete():
#     print("Crawling process completed!")

# process.signals.connect(on_crawler_complete, signal=process.signals.crawler_complete)