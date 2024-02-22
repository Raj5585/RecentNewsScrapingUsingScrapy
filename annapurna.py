import scrapy
from scrapy.crawler import CrawlerProcess

class annapurna(scrapy.Spider):
    name="annapurna"
    start_urls = ['https://www.annapurnapost.com/']

    def __init__(self):
        self.news=[]
        self.f_annapurna()

    def parse(self, response):
        for article in response.xpath(self.article_xpath):
            title=article.xpath(self.title_xpath).get().replace('\n','').strip()
            get_link=article.xpath(self.link_xpath).attrib['href']
            link=f"https://www.annapurnapost.com{get_link}"
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath(self.main_section_xpath)
        #/div[contains(@class, 'description')]/div/figure/img/@data-src"
        img_src=main_section.xpath(self.img_src_xpath).get()
        print(img_src)
        desc=response.xpath(self.description_xpath)

        description=""
        for item in desc:
            description = description + item.xpath('.//text()').get()+"\n"
            if len(description.split())>60:
                description=description.strip()
                break
        print(f"\n\nDescription{description}\n\n")
      
        date=main_section.xpath(self.date_xpath).get()
        self.news.append({'title':title,'description':description,'date':date,'img_src':img_src,'link':link,'newspaper':'Annapurna' })
        print(self.news)

    def f_annapurna(self):
        self.article_xpath='//div[@class="breaking__news"]'
        self.title_xpath='.//h1/a/text()'
        self.link_xpath='.//h1/a'
        self.main_section_xpath='//div[@class="ap__news-content"]'
        self.img_src_xpath='//div[contains(@class,"img__withSound")]/figure/img/@src'
        self.description_xpath='//div[@class="news__details"]/p'
        self.date_xpath='//p[@class="date"]/span/text()'

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'LOG_ENABLED': False,  
            'LOG_STDOUT': False,   
        })
    process.crawl(annapurna)
    process.start()
