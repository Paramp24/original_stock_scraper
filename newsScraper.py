import requests
import re
from bs4 import BeautifulSoup

class NewsScraper:
    def __init__(self):
        pass
    def scrape_text(self, quote):
        url = 'https://www.webull.com/quote/' + quote

        response = requests.get(url)
        return response.text
    
    def get_news_titles(self, quotes):
        pattern = r'"title":\s*"([^"]+)"'
        matches = re.findall(pattern, self.scrape_text(quotes))
        return matches[:11]
    
 