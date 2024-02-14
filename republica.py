import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime


class myRepublica(scrapy.Spider):
    name="republica"
    start_urls = ['https://myrepublica.nagariknetwork.com/']
    def __init__(self):
        self.republica()
        self.news=[]


    def parse(self, response):
       for article in response.xpath(self.article_xpath):
            title=article.xpath(self.title_xpath).get()
            get_link=article.xpath(self.link_xpath).attrib['href']
            link=f"https://myrepublica.nagariknetwork.com{get_link}"
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath(self.main_section_xpath)
        img_src=main_section.xpath(self.img_src_xpath).attrib['src']
        desc=response.xpath(self.description_xpath).getall()
        merged_paragraph = ''.join(desc)
        description=merged_paragraph.split(":")[1]
        date=main_section.xpath(self.date_xpath).getall()[1].strip()
        index=date.find("NPT")
        formatted_date=date[:index]

        self.news.append({'title':title,'description':description,'date':formatted_date,'img_src':img_src,'link':link,'newspaper':'My Republica' })

    def republica(self):
        self.article_xpath='//div[@class="banner top-breaking"]'
        self.title_xpath='.//a/h2/text()'
        self.link_xpath='.//a'
        self.main_section_xpath='//div[@class="box recent-news-categories-details"]'
        self.img_src_xpath='.//div[@class="inner-featured-image"]/img'
        self.description_xpath='//div[@id="newsContent"]/p/text()'
        self.date_xpath='//div[@class="headline-time pull-left"]/p/text()'

process = CrawlerProcess()
process.crawl(myRepublica)
process.start()
