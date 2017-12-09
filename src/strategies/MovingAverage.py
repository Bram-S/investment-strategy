import src.data.StockData as stockData
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MovingAverage:
    short_window = 40
    long_window = 100
    short_av_column = 'short_moving_average'
    long_av_column = 'long_moving_average'
    signal_column = 'signal'
    positions_column = 'positions'

    def __init__(self, market_code, ticker):
        self.ticker = ticker
        self.market_code = market_code
        self.data = stockData.StockData(market_code, ticker)
        self.signals = pd.DataFrame(index=self.data.data.index)
        self.signals[self.signal_column] = 0

    def run(self):
        data_close = self.data.adjusted_close()
        self.signals[self.short_av_column] = data_close.rolling(window=self.short_window, min_periods=1).mean()
        self.signals[self.long_av_column] = data_close.rolling(window=self.long_window, min_periods=1).mean()
        condition = self.signals[self.short_av_column][self.short_window:] > self.signals[self.long_av_column][
                                                                             self.short_window:]
        self.signals.loc[self.short_window:, self.signal_column] = np.where(condition, 1, 0)
        self.signals[self.positions_column] = self.signals[self.signal_column].diff()

    def plot(self):
        self.run()

        fig = plt.figure()

        ax1 = fig.add_subplot(111, ylabel='Price in €')
        self.data.adjusted_close().plot(ax=ax1, color='r', lw=2.)

        self.signals[[self.short_av_column, self.long_av_column]].plot(ax=ax1, lw=2.)

        buy_signals = self.signals.loc[self.signals[self.positions_column] == 1.0]
        ax1.plot(buy_signals.index, buy_signals[self.short_av_column], '^', markersize=10, color='m')

        sell_signals = self.signals.loc[self.signals[self.positions_column] == -1.0]
        ax1.plot(sell_signals.index, sell_signals[self.short_av_column], 'v', markersize=10, color='k')

        plt.show()


if __name__ == '__main__':
    strategy = MovingAverage('BR', 'KBC')
    strategy.plot()
