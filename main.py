from Onlinekhabar import onlinekhabar
from Ratopati import Ratopati

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_ENABLED': False,  
        'LOG_STDOUT': False,   
    })
    
  
    process.crawl(onlinekhabar)
    process.crawl(Ratopati)
    process.start()
 