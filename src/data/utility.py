import os
import settings
import pandas as pd
import src.data.dates as dates


def ticker_csv_path(ticker, market_code):
    return os.path.join(market_path(market_code), ticker + '.csv')


def market_path(market_code):
    return os.path.join(settings.RESOURCES_ROOT, market_code)


def get_data_from_csv(path):
    return pd.read_csv(path, parse_dates=['Date'], date_parser=dates.date_parser)
