import pandas as pd
import os
import settings
import src.data.StockData as StockData


class Market:
    def __init__(self, code):
        self.code = code
        self.path = os.path.join(settings.RESOURCES_ROOT, code)
        self.stocks_datas = pd.Series({})

    def get_stock_names(self):
        stocks = []

        for stock_file in os.listdir(self.path):
            if stock_file.endswith('.csv'):
                stocks.append(stock_file[:-4])

        return stocks

    def load_stocks_datas(self):
        stocks_datas = {}

        for stock_name in self.get_stock_names():
            stocks_datas[stock_name] = self.load_stock_data(stock_name)

        self.stocks_datas = pd.Series(stocks_datas)

    def load_stock_data(self, ticker):
        return StockData.StockData(self.code, ticker)

    def get_stock_data(self, ticker):
        if ticker not in self.stocks_datas:
            self.stocks_datas[ticker] = self.load_stock_data(ticker)

        return self.stocks_datas.at['ticker']
