# import scrapy
# from scrapy.crawler import CrawlerProcess

# data = []
# class Ekantipur(scrapy.Spider):
#     name = 'Ekantipur'
#     start_urls = ['https://ekantipur.com/']

#     def start_request(self):
#         urls = ['https://ekantipur.com/']
#         for url in urls:
#             scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         for links in response.xpath('//section[@class="main-news layout1"]/div/article/h2'):
#             link = links.css('a').attrib["href"]
#             print(link)
#             if link:
                
#                 yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

#     def parse_link(self, response):
#         dict = {}
    

 
#         print(image)
#         print(date)
     
#         dict['Link'] = response.meta['link']
#         dict['Newspaper'] = 'Ekantipur'
#         dict['Title'] = title.replace('\n', '')
#         dict['image'] = image
#         dict['paragraph'] = merged_paragraph
#         dict['date'] = date
#         data.append(dict)
#         print(data)

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_ENABLED': False,  
        'LOG_STDOUT': False,   
    })

    process.crawl(Ekantipur)
    process.start()
 


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