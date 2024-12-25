from flask import Flask, render_template, request, jsonify
from newsScraper import NewsScraper
from Main import get_stock_data, get_trending_stock_scraper

class GUIClass:
    def __init__(self):
        self.app = Flask(__name__, template_folder="templates")

        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if(request.method == 'GET'):
                stock_data = get_stock_data()  # Fetch fresh stock data from the server
                prefered_stock_data = get_trending_stock_scraper()  # Fetch fresh preferred stock data from the server
                return render_template('index.html', stock_data=stock_data, prefered_stock_data=prefered_stock_data)
            else:
                requested_stock_data = request.json  # Get the JSON data from the request body
                news_scraper = NewsScraper()
                response_data = news_scraper.get_news_titles(requested_stock_data)
                return jsonify(response_data)
                
if __name__ == '__main__':
    gui = GUIClass()
    gui.app.run(host='0.0.0.0', port=5000, debug=True)
