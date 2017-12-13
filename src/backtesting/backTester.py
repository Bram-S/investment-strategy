import pandas as pd
import src.strategies.MovingAverage as movingAverage
import matplotlib.pyplot as plt


class BackTester:
    initial_capital = 2e4
    holdings_column = 'holdings'
    cash_column = 'cash'
    total_column = 'total'
    returns_column = 'returns'

    def __init__(self, strategy):
        self.strategy = strategy
        self.strategy.run()
        self.signals = self.strategy.signals
        self.positions = pd.DataFrame(index=self.signals.index)
        self.positions[self.strategy.ticker] = 100 * self.signals.signal
        buy_sell_costs = self.positions.diff().multiply(self.strategy.data.adjusted_close(), axis=0)

        self.portfolio = pd.DataFrame(index=self.signals.index)
        self.portfolio[self.holdings_column] = self.positions.multiply(self.strategy.data.adjusted_close(), axis=0)
        self.portfolio[self.cash_column] = self.initial_capital - buy_sell_costs.cumsum()
        self.portfolio[self.total_column] = self.portfolio[self.cash_column] + self.portfolio[self.holdings_column]
        self.portfolio[self.returns_column] = self.portfolio[self.total_column].pct_change()

    def plot(self):
        figure = plt.figure()
        ax1 = figure.add_subplot(111, ylabel='Portfolio value in €')

        self.portfolio[self.total_column].plot(ax=ax1, lw=2)

        ax1.plot(self.portfolio.loc[self.signals.positions == 1.0].index,
                 self.portfolio.total[self.signals.positions == 1.0], '^', markersize=10, color='m')
        ax1.plot(self.portfolio.loc[self.signals.positions == -1.0].index,
                 self.portfolio.total[self.signals.positions == -1.0], 'v', markersize=10, color='k')
        plt.show()


if __name__ == '__main__':
    ma_strat = movingAverage.MovingAverage('BR', 'KBC')
    back_test = BackTester(ma_strat)
    back_test.plot()
