import requests
from bs4 import BeautifulSoup

class scraperClass:
    def __init__(self):
        pass    # No need to asssign attribute to such a class

    def top_gainers(self, booleanGetGainers):
        
        if booleanGetGainers == True:
            url = "https://www.webull.com/quote/us/gainers"
        else:
            url = "https://www.webull.com/quote/us/dropers"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the elements containing the stock data
        top_gainers_array = soup.find_all(class_="table-cell")

        # Find the elements containing the Change data
        change_1d_value = [tag.text for sublist in top_gainers_array for tag in sublist if "%" in tag.text]    
        change_1d_value = change_1d_value[::2]

        # Find the elements containing the Ticker data and get the text of that
        top_gainers_ticker_symbol_array = soup.find_all(class_="tit bold")
        top_gainers_ticker_symbol_array = [tag.text for tag in top_gainers_ticker_symbol_array]

        # Find the elements containing the Company name and clean the unesscary data and get the text of that
        top_gainers_company_name_symbol_array = soup.find_all(class_="txt") # need to clean
        del top_gainers_company_name_symbol_array[::2]
        top_gainers_company_name_symbol_array = [tag.text for tag in top_gainers_company_name_symbol_array]

        # Get the links to those stocks
        ticker_links_array = soup.find_all('a')
        unfiltered_link_array = [element for element in ticker_links_array if "https://www.webull.com/quote/" in str(element.get("href")) and "-" in str(element.get("href"))]

        #From the links it scrap which exchange it is listed in
        exchanges = []
        for link in unfiltered_link_array:
            exchange = link.get("href").split("/")[4].split("-")[0]
            exchanges.append(exchange)  # Output: "nasdaq"

        #From every a tag, this scraps the href attribute
        ticker_link_array = [element for element in ticker_links_array if len(element.attrs) == 1]
        ticker_filtered_link_array = [tag.get('href') for tag in ticker_link_array]

        # Find the elements containing the Market Cap data
        market_cap_elements = top_gainers_array[10::11]
        market_cap = [tag.text for tag in market_cap_elements]

        #Find The Price
        scraped_prices = top_gainers_array[5::11]
        filtered_prices = [tag.text for tag in scraped_prices]

        #Merges the stock data information with its respective index in a array
        merged_array = [[a, b, c, d, e, f, g] for a, b, c, d, e, f, g in zip(top_gainers_ticker_symbol_array, top_gainers_company_name_symbol_array, change_1d_value, exchanges, ticker_filtered_link_array, market_cap, filtered_prices)]

        #reorganizes the array using the market cap values and returns the highest and lowest value of those
        sorted_array = self.get_lowMC_and_highMC_Stocks(merged_array)

        return sorted_array

    def get_lowMC_and_highMC_Stocks(self, merged_array):
        
        sorted_array = sorted(merged_array, key=lambda x: self.get_numeric_value(x[-1]))

        lowest_MC_Stock = sorted_array[:5]
        highest_MC_Stock = sorted_array[-5:]

        combined_array = lowest_MC_Stock + highest_MC_Stock 
        return combined_array
    
    def get_numeric_value(self, value):
        try:
            if value[-1] == 'M':
                return float(value[:-1]) * 1e6
            elif value[-1] == 'B':
                return float(value[:-1]) * 1e9
            elif value[-1] == 'T':
                return float(value[:-1]) * 1e12
            else:
                return float(value)
        except ValueError:
            return 0


