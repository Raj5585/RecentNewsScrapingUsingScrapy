import scrapy
from scrapy.crawler import CrawlerProcess

class Ekantipur(scrapy.Spider):
    name = 'Ekantipur'
    
    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.start_urls = ['https://www.onlinekhabar.com/']
        self.data = []
        self.titlePath = '//div[@class="article-header"]/h1/text()'
        self.imagepath = "//div[contains(@class, 'description')]/div/figure/img/@data-src"
        self.paragraphpath= '//div[@class="description current-news-block"]/p/text()'
        self.datepath = '//div[@class="time-author"]/time/text()'
       


    def start_request(self):
        yield scrapy.Request(url= self.start_urls, callback=self.parse)

    def parse(self, response):
        for links in response.xpath('//div[@class="span-5 "]/div'): #main div
            link = links.css('a').attrib["href"]
            if link:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        dict = {}
        title = response.xpath(self.titlePath).get()
        image = response.xpath(self.imagepath).get()
        paragraph = response.xpath(self.paragraphpath).getall()
        merged_paragraph = ''.join(paragraph)
        date = response.xpath(self.datepath).get()
        if date == None:
            date = response.xpath('//div[@class="col-xs-12 col-sm-12 col-md-12"]/time/text()').get()

        dict = {'Link':response.meta['link'], 'Newspaper' :'Ratopati','Title': title.replace('\n', ''), 'image' : image,'paragraph': merged_paragraph,'date':date}
        self.data.append(dict)
        print(self.data)
