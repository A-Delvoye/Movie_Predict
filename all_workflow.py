import pandas as pd
from app.schemas.predict_functions import start_prediction
from run_scraping import run_spider

def scraping2predictions()->None:
    """
    1/ trample csv file with weekly_scraping.csv done by run_scraping.py
    2/ Use the prediction model
    3/ trample final_csv_data 
    """
    spider_name = "weekly_spider"
    output_name = "weekly_spider.csv"
    run_spider(spider_name, output_name)
    start_prediction()
    print(start_prediction())
    print("prediction done")

if __name__ == "__main__":
    scraping2predictions()
    

