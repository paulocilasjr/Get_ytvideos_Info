from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from getvideos.spiders.getvideos_spider import GetvideosSpiderSpider
 
 
def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(GetvideosSpiderSpider)
    process.start()

if __name__ == '__main__':
    main()