import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import os
import settings
import src.data.StockData as StockData
import json
import datetime
import time


class Market:
    start_date = '1990-01-01'
    data_source = 'yahoo'

    def __init__(self, code):
        self.code = code
        self.path = os.path.join(settings.RESOURCES_ROOT, code)
        self.stocks_data = pd.Series({})
        self.stock_names = self._get_stock_names()

        with open(os.path.join(self.path, 'config.json')) as config:
            config = json.load(config)

        self.name = config['market_name']
        self.stocks_file = config["all_stocks_file"]

    def _get_stock_names(self):
        stocks = []

        for stock_file in os.listdir(self.path):
            if stock_file.endswith('.csv'):
                stocks.append(stock_file[:-4])

        return stocks

    def load_stocks_data(self):
        stocks_data = {}

        for stock_name in self.stock_names:
            stocks_data[stock_name] = StockData.StockData(self.code, stock_name)

        self.stocks_data = pd.Series(stocks_data)

    def get_stock_data(self, stock_name):
        if stock_name not in self.stocks_data:
            self.stocks_data[stock_name] = StockData.StockData(self.code, stock_name)

        return self.stocks_data.at[stock_name]

    def download_all_stock_data(self):
        for stock_name in self.read_all_stock_names():
            self.download_stock_data(stock_name)

    def read_all_stock_names(self):
        path = os.path.join(settings.RESOURCES_ROOT, self.stocks_file)
        stock_names_data = pd.read_csv(path, sep='\t')

        return stock_names_data.loc[stock_names_data['Market'] == self.name]['Symbol']

    def download_stock_data(self, stock_name):
        path = os.path.join(self.path, stock_name + '.csv')

        if not os.path.isfile(path):
            print('getting ' + stock_name)
            try:
                self.download_stock_data_core(stock_name).to_csv(path)
            except RemoteDataError:
                print("Retrying in 30 seconds")
                time.sleep(30)
                try:
                    self.download_stock_data_core(stock_name).to_csv(path)
                except RemoteDataError:
                    print("Giving up on " + stock_name)
                    return

    def download_stock_data_core(self, stock_name):
        end_date = datetime.datetime.now()

        return data.DataReader(stock_name + "." + self.code, self.data_source, self.start_date, end_date)


if __name__ == '__main__':
    market = Market('BR')
    market.download_all_stock_data()
