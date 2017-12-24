import src.data.StockData as stockData
import pandas as pd
import matplotlib.pyplot as plt


class BuyAndHold:
    signal_column = 'signal'
    positions_column = 'positions'

    def __init__(self, market_code, ticker):
        self.ticker = ticker
        self.market_code = market_code
        self.data = stockData.StockData(market_code, ticker)
        self.signals = pd.DataFrame(index=self.data.data.index)

    def run(self):
        self.signals[self.signal_column] = 1
        self.signals[self.positions_column] = 0
        self.signals[self.positions_column][0] = 1

    def plot(self):
        self.run()

        fig = plt.figure()

        ax1 = fig.add_subplot(111, ylabel='Price in €')
        self.data.adjusted_close().plot(ax=ax1, color='r', lw=2.)

        plt.show()


if __name__ == '__main__':
    strategy = BuyAndHold('BR', 'KBC')
    strategy.plot()
