import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import src.data.allMarketStocks as allStocks
import os
import settings
import src.data.StockData as StockData
import datetime


class Market:
    start_date = datetime.date(1990, 1, 1)
    data_path = 'data'
    actions_path = 'actions'
    data_source = 'yahoo'
    actions_source = 'yahoo-actions'

    def __init__(self, code):
        self.code = code
        self.path_root = os.path.join(settings.RESOURCES_ROOT, code)
        self.data_path = os.path.join(self.path_root, self.data_path)
        self.actions_path = os.path.join(self.path_root, self.actions_path)
        self.stock_names = self._get_stock_names()
        self.stocks_data = self.load_stocks_data()

    def _get_stock_names(self):
        stocks = []

        for stock_file in os.listdir(self.data_path):
            if stock_file.endswith('.csv'):
                stocks.append(stock_file[:-4])

        return stocks

    def load_stocks_data(self):
        stocks_data = {}

        for stock_name in self.stock_names:
            stocks_data[stock_name] = StockData.StockData(self.code, stock_name)

        return pd.Series(stocks_data)

    def get_stock_data(self, stock_name):
        if stock_name not in self.stock_names:
            raise ValueError

        if stock_name in self.stocks_data.index:
            return self.stocks_data.at[stock_name]

        return StockData.StockData(self.code, stock_name)

    def download_all_stock_data(self, update_limit=1, data_type='data'):
        if data_type == 'actions':
            source = self.actions_source
            path_root = self.actions_path
        else:
            source = self.data_source
            path_root = self.data_path
        end_date = datetime.datetime.today().date()

        for stock_name in allStocks.read_all_stock_names(self.code):
            path = os.path.join(path_root, stock_name + '.csv')
            if os.path.isfile(path):
                stock_data = self.get_stock_data(stock_name)
                stock_data = self._update_stock_data(stock_data, source, stock_name, end_date, update_limit)
                stock_data.to_csv(path)
            else:
                stock_data = self._download_stock_data(stock_name, source, self.start_date, end_date, update_limit)
                stock_data.to_csv(path)

    def _update_stock_data(self, stock_data, data_source, stock_name, end_date, update_limit):
        start_date = stock_data.end_date()
        new_data = self._download_stock_data(stock_name, data_source, start_date, end_date, update_limit)
        concatenated = pd.concat([stock_data.data, new_data])

        return concatenated[~concatenated.duplicated()]

    def _download_stock_data(self, stock_name, data_source, start_date, end_date, update_limit):
        stock_data = None

        if (end_date - start_date).days > update_limit:
            if start_date != end_date:
                print('Downloading ' + stock_name)
                try:
                    stock_data = self._download_stock_data_core(stock_name, data_source, start_date, end_date)
                except RemoteDataError:
                    print("Giving up on " + stock_name)

        return stock_data

    def _download_stock_data_core(self, stock_name, data_source, start_date, end_date):
        url_code = stock_name + "." + self.code
        # TODO this will return data before start_date when no new data exists => don't add results in this case,
        # if we do it leads to copied lines of the same date as in e.g. MOPF.csv
        # update: KBC also contains multiple lines with same date
        return data.DataReader(url_code, data_source, start_date, end_date, retry_count=3, pause=3)

    def momenta(self, months=12):
        momenta = {}
        volumes = {}

        for stock_data in self.stocks_data:
            if stock_data.number_of_whole_months() >= months:
                momenta[stock_data.ticker] = stock_data.last_months_total_return(months)
                volumes[stock_data.ticker] = stock_data.last_months_mean_volume(months)

        result = pd.DataFrame({'Momentum': momenta, 'Mean Volume': volumes}).sort_values(by=['Momentum'])
        result.to_csv(os.path.join(settings.RESOURCES_ROOT, 'out', 'momenta.csv'))


if __name__ == '__main__':
    Market('BR').download_all_stock_data(data_type='actions')
