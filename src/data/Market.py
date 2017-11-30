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
    # start_date = '1990-01-01'
    start_date = datetime.date(1990, 1, 1)
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
        if stock_name not in self.stock_names:
            raise ValueError

        if stock_name in self.stocks_data.index:
            return self.stocks_data.at[stock_name]

        return StockData.StockData(self.code, stock_name)

    def read_all_stock_names(self):
        path = os.path.join(settings.RESOURCES_ROOT, self.stocks_file)
        stock_names_data = pd.read_csv(path, sep='\t')

        return stock_names_data.loc[stock_names_data['Market'] == self.name]['Symbol']

    def download_all_stock_data(self):
        end_date = datetime.datetime.today().date()

        for stock_name in self.read_all_stock_names():
            path = os.path.join(self.path, stock_name + '.csv')
            if os.path.isfile(path):
                # TODO now all data starts from the old start date => fix
                stock_data = self.update_stock_data(self.get_stock_data(stock_name), stock_name, end_date, path)
            else:
                stock_data = self.download_stock_data(stock_name, self.start_date, end_date, path)

            if stock_data is not None:
                stock_data.to_csv(path)

    def update_stock_data(self, stock_data, stock_name, end_date, path):
        start_date = stock_data.end_date()
        new_data = self.download_stock_data(stock_name, start_date, end_date, path)

        return pd.concat([stock_data.data, new_data])

    def download_stock_data(self, stock_name, start_date, end_date, path):
        if start_date != end_date:
            print('Downloading ' + stock_name)
            try:
                stock_data = self.download_stock_data_core(path, stock_name, start_date, end_date)
            except RemoteDataError:
                print("Retrying " + stock_name + " in 30 seconds")
                time.sleep(30)
                try:
                    stock_data = self.download_stock_data_core(path, stock_name, start_date, end_date)
                except RemoteDataError:
                    print("Giving up on " + stock_name)

        return stock_data

    def download_stock_data_core(self, path, stock_name, start_date, end_date):
        # TODO experiment with pause and retry parameters to avoid having to do error checking in calling method
        return data.DataReader(stock_name + "." + self.code, self.data_source, start_date, end_date)


if __name__ == '__main__':
    Market('BR').download_all_stock_data()
