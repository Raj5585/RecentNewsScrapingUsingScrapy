import scrapy
data = []
papername = 'OnlineKhabar'
class onlinekhabar(scrapy.Spider):
    name = 'onlinekhabar'
    start_urls = ['https://www.onlinekhabar.com/']

    def start_request(self):
        urls = ['https://www.onlinekhabar.com/']
        for url in urls:
            scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for links in response.xpath('//div[@class="span-5 "]/div'):
            link = links.css('a').attrib["href"]
            print(link)
            if link:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        dict = {}
        title = response.xpath('//div[@class="ok-post-title-right"]/h1/text()').get()
        image = response.xpath('//div[@class="post-thumbnail"]/img/@src').get()
        paragraph = response.xpath('//div[@class="ok18-single-post-content-wrap"]/p/text()').getall()
        date = response.xpath('//div[@class="ok-post-title-right"]/div[@class="ok-title-info flx"]/div[@class="ok-news-post-hour"]/span/text()').get()
        # print(title)
        # print(image)
        # print(paragraph)
        # print(date)
        dict['Link'] = response.meta['link']
        dict['Newspaper'] = papername
        dict['Title'] = title.replace('\n', '')
        dict['image'] = image
        dict['paragraph'] = paragraph[0:3]
        dict['date'] = date
        data.append(dict)


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    process.crawl(onlinekhabar)
    process.start()
    print(data)