import requests
import re

class preferedStockScraper:
    def __init__(self, topTrendingStocks, findKeys) :
        self.topTrendingStock = topTrendingStocks
        self.findKeys = findKeys

    def find_numbers_with_suffix_between_divs(self, long_string):
        pattern = r'(\d+(?:\.\d+)?(?:[MmBbTt]))</div>'
        matches = re.findall(pattern, long_string)
        return matches

    def calculate_stock_percentage_change(self, current_price, change):
        percentage_change = (change / current_price) * 100
        return str(round(percentage_change, 2)) + '%'

    def get_market_cap(self, data_string):
        numbers_between_divs = self.find_numbers_with_suffix_between_divs(data_string)
        return (numbers_between_divs[1])

    def clean_data(self, string_value):
        stripped_string_value = string_value.strip('"')
        float_value = float(stripped_string_value)
        return float_value

    def clean_extra_quotations(self, array):
        cleaned_data = [item.strip('"') for item in array]
        return cleaned_data

    def scrape_website(self, x):
        searchURL = 'https://www.webull.com/quote/' + x

        response = requests.get(searchURL)
        data_string = response.text
        stock_information = []

        for i in self.findKeys:

            start_index = data_string.find(i)
            start_index += len(i)

            end_index = data_string.find(',', start_index)

            if end_index != -1:
                derivative_support = str(data_string[start_index:end_index])
                stock_information.append(derivative_support)
        
        change = (self.calculate_stock_percentage_change(self.clean_data(stock_information[4]), self.clean_data(stock_information[3])))
        
        stock_information.append(searchURL)
        stock_information.append(change)
        stock_information.append(self.get_market_cap(data_string))
        
        stock_information.pop(3)
        stock_information.pop(4)
        return self.clean_extra_quotations(stock_information)

    def scrapePreferedStock(self):

        totalStockInformation = []

        for i in self.topTrendingStock:
            
            totalStockInformation.append(self.scrape_website(i))
        
        return totalStockInformation
