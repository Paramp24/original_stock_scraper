from scraperClass import scraperClass
from blueChipScraper import preferedStockScraper

def get_stock_data():

    my_scraper = scraperClass()

    gainers_data = my_scraper.top_gainers(True) # Get Top Gainer Stocks
    droppers_data = my_scraper.top_gainers(False) # Gets Top Loser Stocks

    stock_data = [gainers_data, droppers_data]
    return stock_data

def get_trending_stock_scraper():

    topTrendingStocks = ['nasdaq-aapl', 'nasdaq-goog', "nasdaq-googl", 'nasdaq-msft', 'nasdaq-amzn', 'nasdaq-tsla', 'nasdaq-nvda', 'nyse-uber']
    findKeys = ['"symbol":', '"name":', '"disExchangeCode":', '"change":', '"close":']

    trending_stock_scraper = preferedStockScraper(topTrendingStocks, findKeys)
    prefered_stock_data = trending_stock_scraper.scrapePreferedStock()
    return prefered_stock_data
#create a mega class that conrols all class and one main pthon document that reads that class