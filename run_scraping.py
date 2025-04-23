from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os




def run_spider(
    spider_name: str,    
    output_name: str,
) -> None:
    """Outputs are placed in root/data_scraping/output_name."""

    output_path = "data_scraping/" + output_name


    # 👇 Supprimer le fichier s'il existe
    if os.path.exists(output_path):
        os.remove(output_path)

    settings = get_project_settings()

    settings.set("FEED_URI", output_path)
    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()


if __name__ == "__main__":
    spider_name = "weekly_spider"
    output_name = "weekly_spider.csv"

    run_spider(
        spider_name, output_name
    )