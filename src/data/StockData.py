import os
import settings
import pandas as pd
import src.data.dates as dates
import matplotlib.pyplot as plt
import numpy as np


class StockData:
    date_column = 'Date'
    adj_close_column = 'Adj Close'
    volume_column = 'Volume'

    def __init__(self, market_code, ticker):
        self.ticker = ticker
        self.market_code = market_code
        self.path = os.path.join(settings.RESOURCES_ROOT, market_code, ticker + '.csv')
        csv_data = self.load_data_csv()
        self.data = csv_data[~csv_data.index.duplicated()]

    def load_data_csv(self):
        csv = pd.read_csv(self.path, index_col=self.date_column, parse_dates=[self.date_column],
                          date_parser=dates.date_parser)
        return csv

    def end_date(self):
        return self.data.index[-1].date()

    def adjusted_close(self):
        return self.data[self.adj_close_column]

    def plot(self):
        self.adjusted_close().plot(grid=True)
        plt.show()

    def daily_returns(self):
        return self.adjusted_close().pct_change().fillna(0)

    def monthly_returns(self):
        return self.adjusted_close().resample('BM', convention='end').asfreq().pct_change()

    def last_months_total_return(self, months):
        month_returns = self.monthly_returns()[-months - 1:-1]
        cum_returns = (1 + month_returns).cumprod()

        return cum_returns[-1] - 1

    def last_months_mean_volume(self, months):
        return self.data[self.volume_column].resample('BM', convention='end').asfreq()[-months - 1:-1].mean()

    def cumulative_daily_returns(self):
        return (1 + self.daily_returns()).cumprod()

    def daily_log_returns(self):
        return np.log(1 + self.daily_returns())

    def returns_outliers(self, threshold=10):
        returns = self.daily_returns()
        z_scores = self.returns_modified_z_scores()

        return returns[z_scores.abs() > threshold]

    def returns_modified_z_scores(self):
        returns = self.daily_returns()
        return 0.6745 * (returns - returns.median()) / self.returns_mad()

    def returns_mad(self):
        returns = self.daily_returns()
        return (returns - returns.median()).abs().median()

    def number_of_whole_months(self):
        start_date = self.data.index[0]
        end_date = self.data.index[-1]

        return max(0, 12 * (end_date.year - start_date.year) + end_date.month - start_date.month - 1)


if __name__ == '__main__':
    data = StockData('BR', 'ABI')
    data.last_months_total_return(12)
    # TODO 'BR' 'PROX' has very big outliers => we need a way to remove outliers
    # also BEAB weird in beginning
