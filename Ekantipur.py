import scrapy
data = []
class Ekantipur(scrapy.Spider):
    name = 'Ekantipur'
    start_urls = ['https://ekantipur.com/']

    def start_request(self):
        urls = ['https://ekantipur.com/']
        for url in urls:
            scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for links in response.xpath('//section[@class="main-news layout1"]/div/article/h2'):
            link = links.css('a').attrib["href"]
            print(link)
            if link:
                
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        dict = {}
        title = response.xpath('//div[@class="article-header"]/h1') #/text()').get()
        image = response.xpath("//div[contains(@class, 'description')]/div/figure/img/@data-src").get()
        
        paragraph = response.xpath('//div[@class="description current-news-block"]/p/text()').getall()
        date = response.xpath('//div[@class="time-author"]/time/text()').get()
        if date == None:
            date = response.xpath('//div[@class="col-xs-12 col-sm-12 col-md-12"]/time/text()').get()

 
        print(image)
        print(date)
     
        dict['Link'] = response.meta['link']
        dict['Newspaper'] = 'Ekantipur'
        dict['Title'] = title.replace('\n', '')
        dict['image'] = image
        dict['paragraph'] = paragraph[0:3]
        dict['date'] = date
        data.append(dict)
        print(data)

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_ENABLED': False,  
        'LOG_STDOUT': False,   
    })

    process.crawl(Ekantipur)
    process.start()
    print(data)