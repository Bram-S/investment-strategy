from pandas_datareader import data
import os
import settings
import datetime


def get_brussels_historical_data(ticker):
    start_date = '2008-01-01'
    end_date = datetime.datetime.now()
    data_source = 'yahoo'

    return data.DataReader(ticker + '.BR', data_source, start_date, end_date)


def save_data_to_csv(ticker):
    path = os.path.join(settings.RESOURCES_ROOT, ticker + '.csv')
    get_brussels_historical_data(ticker).to_csv(path)


if __name__ == '__main__':
    save_data_to_csv('VALOR')
