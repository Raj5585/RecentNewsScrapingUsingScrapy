import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime



class KathmanduPost(scrapy.Spider):
    name="kathmandu_post"
    start_urls = ['https://kathmandupost.com']

    def __init__(self):
        self.news = []
        self.kathmandu_post()

    def parse(self, response):
        main_div = response.xpath(self.main_div_xpath)
        articles = main_div.xpath(self.article_xpath)

        for article in articles:
            link = article.xpath(self.link_xpath).attrib['href']
            yield scrapy.Request(url = self.start_urls[0] + link, callback = self.parse_article)


    def parse_article(self, response):
        print("parsing")
        print(f"visiting link {response.url}")
        article = response.xpath(self.main_section_xpath)
        title = article.xpath(self.title_xpath).get().strip()

        article_date = article.xpath(self.date_xpath).get()

        published_date_str = article_date.split(':', 1)[-1].strip()

        try:
            date_object = datetime.strptime(published_date_str, '%B %d, %Y')
            formatted_date = date_object.strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing date: {e}")

        desc=response.xpath(self.description_xpath).getall()
        description = ''.join(desc)
        # print(description)
        print(f"Title: {title}")
        # img_src = response.xpath('//*[@id="mainContent"]/main/div/div[2]/div[1]/img').attrib['src']
        img_src = response.xpath(self.img_src_xpath).get()
        print(f"Img: {img_src}")

        self.news.append({'title':title,'description':description,'date':formatted_date,'img_src':img_src,'link':response.url,'newspaper':'The Kathmandu Post' })
        

    def kathmandu_post(self):
        self.main_div_xpath='//div[@class="col-xs-12 col-sm-6 col-md-4 grid-first divider-right order-2--sm"]'
        self.article_xpath='.//article[contains(@class, "article-image article-image--left")]'
        self.title_xpath='//h1[@style]/text()'
        self.link_xpath='.//a'
        self.main_section_xpath='//div[@class="col-sm-8"]'
        self.img_src_xpath='//div[contains(@class,"row")]/div/img/@data-src'
        self.description_xpath='//section/p/text()'
        self.date_xpath='//div[@class="updated-time"]/text()'

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'LOG_ENABLED': False,  
    'LOG_STDOUT': False,   
})
process.crawl(KathmanduPost)
process.start()
