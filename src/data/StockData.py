import os
import settings
import pandas as pd
import src.data.dates as dates
import matplotlib.pyplot as plt
import numpy as np


class StockData:
    date_column = 'Date'
    adj_close_column = 'Adj Close'

    def __init__(self, market_code, ticker):
        self.ticker = ticker
        self.market_code = market_code
        self.path = os.path.join(settings.RESOURCES_ROOT, market_code, ticker + '.csv')
        self.data = self.load_data_csv()

    def load_data_csv(self):
        csv = pd.read_csv(self.path, index_col=self.date_column, parse_dates=[self.date_column],
                          date_parser=dates.date_parser)
        return csv.dropna()

    def end_date(self):
        return self.data.index[-1].date()

    def adjusted_close(self):
        return self.data[self.adj_close_column]

    def plot(self):
        self.adjusted_close().plot(grid=True)
        plt.show()

    def daily_returns(self):
        return self.adjusted_close().pct_change().fillna(0)

    def cumulative_daily_returns(self):
        return (1 + self.daily_returns()).cumprod()

    def cumulative_monthly_returns(self):
        return self.cumulative_daily_returns().resample('M').mean()

    def daily_log_returns(self):
        return np.log(1 + self.daily_returns())

    def momentum(self, months):
        return None


if __name__ == '__main__':
    data = StockData('BR', 'KBC')
    data.plot()
