from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_spider(
    spider_name: str,    
    output_name: str,
) -> None:

    settings = get_project_settings()

    settings.set("FEED_URI", output_name)
    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()


if __name__ == "__main__":
    spider_name = "weekly_spider"
    output_name = "weekly_spider.csv"

    run_spider(
        spider_name, output_name
    )