import pandas as pd
import src.strategies.MovingAverage as movingAverage
import src.strategies.BuyAndHold as BuyAndHold
import matplotlib.pyplot as plt


class BackTester:
    initial_capital = 2e4
    num_stocks_column = 'stocks'
    holdings_column = 'holdings'
    cash_column = 'cash'
    total_column = 'total'
    returns_column = 'returns'

    def __init__(self, strategy):
        self.strategy = strategy
        self.strategy.run()
        self.signals = self.strategy.signals.fillna(0)
        self.positions = pd.DataFrame(index=self.signals.index)
        num_stocks_and_cash = self.line_per_line()
        self.portfolio = pd.DataFrame(index=self.signals.index)
        num_stocks = num_stocks_and_cash[self.num_stocks_column]
        self.portfolio[self.holdings_column] = num_stocks.multiply(self.strategy.data.adjusted_close(), axis=0)
        self.portfolio[self.cash_column] = num_stocks_and_cash[self.cash_column]
        self.portfolio[self.total_column] = self.portfolio[self.cash_column] + self.portfolio[self.holdings_column]
        self.portfolio[self.returns_column] = self.portfolio[self.total_column].pct_change()

    def line_per_line(self):
        start_cash = self.initial_capital
        stocks_held = pd.Series(index=self.signals.index, name=self.num_stocks_column)
        cash = pd.Series(index=self.signals.index, name=self.cash_column)

        position = self.signals.positions[0]
        adj_close = self.strategy.data.adjusted_close()[0]
        if position > 0:
            stocks_held[0] = start_cash // adj_close
            cash[0] = start_cash - adj_close * stocks_held[0]
        else:
            stocks_held[0] = 0
            cash[0] = start_cash

        for i in range(1, self.signals.index.shape[0]):
            position = self.signals.positions[i]
            adj_close = self.strategy.data.adjusted_close()[i]

            if position > 0:
                stocks_held[i] = cash[i - 1] // adj_close
                cash[i] = cash[i - 1] - adj_close * stocks_held[i]
            elif position < 0:
                stocks_held[i] = 0
                cash[i] = cash[i - 1] + stocks_held[i - 1] * adj_close
            else:
                stocks_held[i] = stocks_held[i - 1]
                cash[i] = cash[i - 1]

        return pd.concat([stocks_held, cash], axis=1)

    def plot(self):
        bench_mark_strategy = BuyAndHold.BuyAndHold(self.strategy.market_code, self.strategy.ticker)
        bench_mark = BackTester(bench_mark_strategy)
        figure = plt.figure()
        ax1 = figure.add_subplot(111, ylabel='Portfolio value in €')

        self.portfolio[self.total_column].plot(ax=ax1, lw=2)
        bench_mark.portfolio[self.total_column].plot(ax=ax1, color='k', lw=1)

        ax1.plot(self.portfolio.loc[self.signals.positions == 1.0].index,
                 self.portfolio.total[self.signals.positions == 1.0], '^', markersize=10, color='m')
        ax1.plot(self.portfolio.loc[self.signals.positions == -1.0].index,
                 self.portfolio.total[self.signals.positions == -1.0], 'v', markersize=10, color='k')
        plt.show()


if __name__ == '__main__':
    # ma_strat = movingAverage.MovingAverage('BR', 'KBC')
    ma_strat = movingAverage.MovingAverage('BR', 'PROX')
    # ma_strat = BuyAndHold.BuyAndHold('BR', 'KBC')
    back_test = BackTester(ma_strat)
    back_test.plot()
