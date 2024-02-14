from typing import Any
import scrapy



class Ratopati(scrapy.Spider):
    name = 'Ratopati'

    def __init__(self, name: str | None = None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = ['https://www.ratopati.com/']
        self.data = []
        self.titlePath = '//div/h2[@class = "heading"]/text()'
        self.imagepath = '//figure[@class = "featured-image"]/img/@src'
        self.paragraphpath= '//div[@class = "the-content"]/p/text()'
        self.datepath = '//div/span[@class="date"]/text()'

    def start_request(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        for div in response.css('.heading.text--black'): #main div css 
            link = div.css('a').attrib["href"] 
            if link:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        title = response.xpath(self.titlePath).get() 
        image = response.xpath(self.imagepath).get()
        paragraph = response.xpath(self.paragraphpath).getall()
        merged_paragraph = ''.join(paragraph)
        date = (response.xpath(self.datepath).get()).split(',')
        dict = {'Link':response.meta['link'], 'Newspaper' :'Ratopati','Title': title.replace('\n', ''), 'image' : image,'paragraph': merged_paragraph,'date':date[1].replace('\n', '')}
        self.data.append(dict)
        print(self.data)
        


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_ENABLED': False,  
        'LOG_STDOUT': False,   
    })
    
  

    process.crawl(Ratopati)
    process.start()