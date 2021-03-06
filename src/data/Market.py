import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import src.data.allMarketStocks as allStocks
import os
import settings
import src.data.StockData as StockData
import datetime
import src.data.stockActions as stockActions


class Market:
    start_date = datetime.date(1990, 1, 1)
    data_folder = 'data'
    actions_folder = 'actions'
    data_source = 'morningstar'
    actions_source = 'yahoo-actions'

    def __init__(self, code):
        self.code = code
        self.path_root = os.path.join(settings.RESOURCES_ROOT, code)

        if not os.path.exists(self.path_root):
            raise ValueError('Invalid market code: ' + self.code)

        self.data_path = os.path.join(self.path_root, self.data_folder)

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.out_path = os.path.join(settings.RESOURCES_ROOT, 'out')
        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path)

        self.actions_path = os.path.join(self.path_root, self.actions_folder)
        self.stock_names = self._get_stock_names()
        self.stocks_data = self.load_stocks_data()

    def _get_stock_names(self):
        stocks = []

        for stock_file in os.listdir(self.data_path):
            if stock_file.endswith('.csv'):
                stocks.append(stock_file[:-4])

        return stocks

    def load_stocks_data(self):
        print('Loading stocks data')
        stocks_data = {}

        for stock_name in self.stock_names:
            stocks_data[stock_name] = StockData.StockData(self.code, stock_name)

        print('Loading stocks data done')

        return pd.Series(stocks_data)

    def get_stock_data(self, stock_name):
        if stock_name not in self.stock_names:
            raise ValueError

        if stock_name in self.stocks_data.index:
            return self.stocks_data.at[stock_name]

        return StockData.StockData(self.code, stock_name)

    def download_all_stock_data(self, update_limit=1, data_type='data'):
        if data_type == 'actions':
            print('Downloading actions')
            source = self.actions_source
            path_root = self.actions_path
        else:
            print('Downloading data')
            source = self.data_source
            path_root = self.data_path

        end_date = datetime.datetime.today().date()

        for stock_name in allStocks.read_all_stock_names(self.code):
            path = os.path.join(path_root, stock_name + '.csv')
            if os.path.isfile(path):
                stock_data = self._update_stock_data(source, stock_name, end_date, update_limit)
            else:
                stock_data = self._download_stock_data(stock_name, source, self.start_date, end_date, update_limit)

            if stock_data is not None:
                stock_data.to_csv(path)

        print('Downloading done')

    def _update_stock_data(self, data_source, stock_name, end_date, update_limit):
        if data_source == self.actions_source:
            old_data = stockActions.StockActions(self.code, stock_name)
        else:
            old_data = self.get_stock_data(stock_name)

        start_date = old_data.end_date()
        new_data = self._download_stock_data(stock_name, data_source, start_date, end_date, update_limit)
        concatenated = pd.concat([old_data.data, new_data]).sort_index()

        return concatenated[~concatenated.index.duplicated()]

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
        url_code = self._url_code(stock_name, data_source)
        try:
            stock_data = data.DataReader(url_code, data_source, start_date, end_date, retry_count=0)
            stock_data.index = stock_data.index.droplevel(0)

            return stock_data.sort_index()
        except (ValueError, TypeError):
            print("No data found for " + stock_name)
            return None

    def _url_code(self, stock_name, data_source):
        if data_source == 'yahoo':
            return stock_name + "." + self.code

        if data_source == 'morningstar':
            return self.code + ":" + stock_name

        raise ValueError('Unexpected data_source: ' + data_source)

    def momenta(self, months=12):
        momenta = {}
        volumes = {}

        for stock_data in self.stocks_data:
            if stock_data.number_of_whole_months() >= months:
                momenta[stock_data.ticker] = stock_data.last_months_total_return(months)
                volumes[stock_data.ticker] = stock_data.last_months_mean_volume(months)

        result = pd.DataFrame({'Momentum': momenta, 'Mean Volume': volumes})
        return result.sort_values(by=['Momentum'], ascending=False)


if __name__ == '__main__':
    Market('XPAR').download_all_stock_data()
    Market('XPAR').momenta()
