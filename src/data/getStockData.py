from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import os
import pandas as pd
import settings
import datetime
import time

start_date = '1990-01-01'
data_source = 'yahoo'
all_stocks_file = 'Euronext_Equities_EU_2017-11-06_clean.csv'
suffix = 'BR'
market_name = 'Euronext Brussels'


def download_all_prices():
    for ticker in get_all_tickers():
        download_and_save(ticker)


def get_all_tickers():
    path = os.path.join(settings.RESOURCES_ROOT, all_stocks_file)

    tickers_data = pd.read_csv(path, sep='\t')

    return tickers_data.loc[tickers_data['Market'] == market_name]['Symbol']


def download_and_save(ticker):
    path = os.path.join(settings.RESOURCES_ROOT, suffix, ticker + '.csv')

    if not os.path.isfile(path):
        print('getting ' + ticker)
        try:
            get_historical_data(ticker).to_csv(path)
        except RemoteDataError:
            print("Retrying in 30 seconds")
            time.sleep(30)
        try:
            get_historical_data(ticker).to_csv(path)
        except RemoteDataError:
            print("Giving up on " + ticker)
            return


def get_historical_data(ticker):
    end_date = datetime.datetime.now()

    return data.DataReader(ticker + "." + suffix, data_source, start_date, end_date)


if __name__ == '__main__':
    download_all_prices()
