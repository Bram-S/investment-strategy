import os
import settings
import matplotlib.pyplot as plt
import numpy as np
import src.data.dataLoader as dataLoader
import src.data.stats as stats
import datetime


class StockData:
    date_column = 'Date'
    adj_close_column = 'Close'
    volume_column = 'Volume'

    def __init__(self, market_code, ticker):
        self.ticker = ticker
        self.market_code = market_code
        # TODO this path is used in Market and here => should set somewhere central
        self.path = os.path.join(settings.RESOURCES_ROOT, market_code, 'data', ticker + '.csv')
        csv_data = dataLoader.load_data_csv(self.path, self.date_column)
        self.data = csv_data[~csv_data.index.duplicated()]

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

    def last_days_outliers(self, days=365):
        start_date = datetime.datetime.today().date() - datetime.timedelta(days=days)
        start_index = self.data.index.get_loc(start_date, method='nearest')

        return stats.outliers(self.adjusted_close()[start_index:].pct_change())

    def cumulative_daily_returns(self):
        return (1 + self.daily_returns()).cumprod()

    def daily_log_returns(self):
        return np.log(1 + self.daily_returns())

    def number_of_whole_months(self):
        start_date = self.data.index[0]
        end_date = self.data.index[-1]

        return max(0, 12 * (end_date.year - start_date.year) + end_date.month - start_date.month - 1)


if __name__ == '__main__':
    data = StockData('XBRU', 'MITRA')
    print(data.end_date())
    data.plot()
