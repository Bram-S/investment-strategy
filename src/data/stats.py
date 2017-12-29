import src.data.utility as utility
import pandas as pd
import os


def get_start_date(ticker, market_code):
    path = utility.ticker_csv_path(ticker, market_code)
    data = utility.get_data_from_csv(path)

    return data.at[0, 'Date']


def get_market_start_dates(market_code):
    market_path = utility.market_path(market_code)
    start_dates = []

    for ticker_file in os.listdir(market_path):
        if ticker_file.endswith('.csv'):
            ticker_data = utility.get_data_from_csv(os.path.join(market_path, ticker_file))
            start_dates.append(ticker_data.at[0, 'Date'])

    return pd.Series(start_dates)


def get_lowest_market_start_date(market_code):
    return get_market_start_dates(market_code).min()


def get_highest_market_start_date(market_code):
    return get_market_start_dates(market_code).max()


def get_end_date(ticker, market_code):
    data = pd.read_csv(utility.ticker_csv_path(ticker, market_code))

    return data.iloc[-1].at['Date']


def mad(series):
    return (series - series.median()).abs().median()


def modified_z_scores(series):
    series_mad = mad(series)

    if mad == 0:
        raise ValueError
        return 0

    return 0.6745 * (series - series.median()) / series_mad


def outliers(series, threshold=10):
    z_scores = modified_z_scores(series)

    return series[z_scores.abs() > threshold]


def momentum(ticker, market_code):
    days_in_month = 22
    path = utility.ticker_csv_path(ticker, market_code)
    data = utility.get_data_from_csv(path)
    # TODO check whether data has more than days_in_month rows
    last_close = data.iloc[-1].at['Adj Close']
    month_start_close = data.iloc[-days_in_month - 1].at['Adj Close']

    return last_close - month_start_close
