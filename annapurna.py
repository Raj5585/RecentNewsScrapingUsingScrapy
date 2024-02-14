import scrapy
from scrapy.crawler import CrawlerProcess


news=[]

class annapurna(scrapy.Spider):
    name="annapurna"
    start_urls = ['https://www.annapurnapost.com/']

    def parse(self, response):
        for article in response.xpath('//div[@class="breaking__news"]'):
            title=article.xpath('.//h1/a/text()').get().replace('\n','').strip()
            get_link=article.xpath('.//h1/a').attrib['href']
            link=f"https://www.annapurnapost.com{get_link}"
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath('//div[@class="ap__news-content"]')
        #/div[contains(@class, 'description')]/div/figure/img/@data-src"
        img_src=main_section.xpath('//div[contains(@class,"img__withSound")]/figure/img/@src').get()
        print(img_src)
        description=response.xpath('//div[@class="news__details"]/p/text()').get()
      
        desc=description.split(":")[1]
      
        date=main_section.xpath('//p[@class="date"]/span/text()').get()
        news.append({'title':title,'description':desc,'date':date,'img_src':img_src,'link':link,'newspaper':'Annapurna' })

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'LOG_ENABLED': False,  
            'LOG_STDOUT': False,   
        })
    process.crawl(annapurna)
    process.start()
    print(news)
    
    def ParagraphMerger(lst):
        lst.split(',')
