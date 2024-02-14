import scrapy

class onlinekhabar(scrapy.Spider):
    name = 'onlinekhabar'
    
    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.start_urls = ['https://www.onlinekhabar.com/']
        self.data = []
        self.titlePath = '//div[@class="ok-post-title-right"]/h1/text()'
        self.imagepath = '//div[@class="post-thumbnail"]/img/@src'
        self.paragraphpath= '//div[@class="ok18-single-post-content-wrap"]/p/text()'
        self.datepath = '//div[@class="ok-post-title-right"]/div[@class="ok-title-info flx"]/div[@class="ok-news-post-hour"]/span/text()'

    def start_request(self):
        yield scrapy.Request(url= self.start_urls, callback=self.parse)

    def parse(self, response):
        for links in response.xpath('//div[@class="span-5 "]/div'):
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
        dict = {'Link':response.meta['link'], 'Newspaper' :'Ratopati','Title': title.replace('\n', ''), 'image' : image,'paragraph': merged_paragraph,'date':date}
        self.data.append(dict)
        print(self.data)


