import scrapy

data = []
Papername = 'ratopati'
class Ratopati(scrapy.Spider):
    name = Papername
    start_urls = ['https://www.ratopati.com/']


    def start_request(self):
        urls = ['https://www.ratopati.com/']
        for url in urls:
            scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for div in response.css('.heading.text--black'):
            link = div.css('a').attrib["href"] 
            if link:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        dict = {}
        title = response.xpath('//div/h2[@class = "heading"]/text()').get()
        image = response.xpath('//figure[@class = "featured-image"]/img/@src').get()
        paragraph = response.xpath('//div[@class = "the-content"]/p/text()').getall()
        date = (response.xpath('//div/span[@class="date"]/text()').get()).split(',')
     
  
        dict['Link'] = response.meta['link']
        dict['Newspaper'] = Papername
        dict['Title'] = title.replace('\n', '')
        dict['image'] = image
        dict['paragraph'] = paragraph[0:3]
        dict['date'] = date[1].replace('\n', '')
        data.append(dict)



if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    
    process.crawl(Ratopati)
    process.start()
    print(data)