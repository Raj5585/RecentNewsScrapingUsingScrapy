import scrapy
from scrapy.crawler import CrawlerProcess

from scrapy.utils.reactor import install_reactor
news = []
# from twisted.internet import asyncioreactor
# asyncioreactor.install()


class AnnapurnaCat(scrapy.Spider):
    name = "AnnapurnaCat"
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    # start_urls = ['https://www.annapurnapost.com/']

    def __init__(self):
        self.articles_xpath = '//div[@class="category__news"]/div[@class="custom-container"]/div[@class="category__news-grid"]'
        self.article_xpath = './/div[@class="grid__card"]'
        self.image_xpath = './/div[@class="card__img"]/a/img/@src'
        self.title_xpath = './/div[@class="card__details"]/h3/a/text()'
        self.article_link_xpath = './/div[@class="card__details"]/h3/a/@href'
        self.main_section_xpath = '//div[@class="ap__news-content"]'
        self.description_xpath = './/div[@class="news__details"]/p/text()'
        self.date_xpath = './/p[@class="date"]/span/text()'
        self.news = []
        self.categories = {
            'politics': r'https://www.annapurnapost.com/category/politics/',
            'society': r'https://www.annapurnapost.com/category/society/',
            'economy': r'https://www.annapurnapost.com/category/economy/',
            'opinion': r'https://www.annapurnapost.com/category/opinion/',

            'sports': r'https://www.annapurnapost.com/category/sports/',
            'entertainment': r'https://www.annapurnapost.com/category/entertainment/',
            'science': r'https://www.annapurnapost.com/category/science/',
            'technology': r'https://www.annapurnapost.com/category/technology/',
            'health': r'https://www.annapurnapost.com/category/health/',
            'lifestyle': r'https://www.annapurnapost.com/category/lifestyle/',
            'education': r'https://www.annapurnapost.com/category/education/',
            'travel': r'https://www.annapurnapost.com/category/travel/',
            'fashion': r'https://www.annapurnapost.com/category/fashion/',
            'business': r'https://www.annapurnapost.com/category/business/',
            'international': r'https://www.annapurnapost.com/category/international/',
            'finance': r'https://www.annapurnapost.com/category/finance/',
            'art': r'https://www.annapurnapost.com/category/art/',
            'weather': r'https://www.annapurnapost.com/category/weather/',
            'others': r'https://www.annapurnapost.com/category/others/'
        }

    def start_requests(self):
        for category in self.categories:
            # print(f"Category:{category}")
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        print("************************************************")
        print(f"Parsing Response on category {response.meta['category']}:")
        # print(response)
        acticles = response.xpath(self.articles_xpath)
        for article in acticles.xpath(self.article_xpath):
            # print(f"Article:{article.get()}")
            image_link = article.xpath(self.image_xpath).get().strip()
            title = article.xpath(self.title_xpath).get().strip()
            get_link = article.xpath(self.article_link_xpath).get()
            link = f"https://www.annapurnapost.com{get_link}"

            yield scrapy.Request(url=link, callback=self.parse_article, meta={'title': title, 'link': link, 'img_link': image_link, 'category': response.meta['category']})
            

    def parse_article(self, response):
        title = response.meta['title']
        link = response.meta['link']
        img_src = response.meta['img_link']
        category = response.meta['category']
        main_section = response.xpath(self.main_section_xpath)
        description_elements = main_section.xpath(self.description_xpath)
        description = ""
        for item in description_elements:
            # print(f"Item:{item.get()}")
            description = description + item.get().strip() + "\n"
            # if len(description.split()) > 60:
            #     description = description.strip()
            #     break
        description = description.strip()
        date = main_section.xpath(self.date_xpath).get()
        # print(f"Date:{date}")
        item = {'title': title,
                'newspaper': 'Annapurna',
                'category': category,
                'date': date,
                'link': link,
                'img_src': img_src,
                'description': description,
                }
        self.news.append(item)

    def closed(self, reason):
        # Print or process items after the crawling process is complete
        print("Items after crawling:")
        for item in self.news:
            for key, value in item.items():
                print(f"{key}:{value}")
            
            # print(f"Title:{item['title']}\nLink:{item['link']}\nDescription:{item['description']}\nImage:{item['img_src']}\nNewspaper:{item['newspaper']}\tDate:{item['date']}\n\n")

# if __name__ == "__main__":
#     from scrapy.crawler import CrawlerProcess
#     process = CrawlerProcess({
#             'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'LOG_ENABLED': False,
#             'LOG_STDOUT': False,
#         })
#     process.crawl(annapurna)
#     process.start()
#     print(news)

#     def ParagraphMerger(lst):
#         lst.split(',')
