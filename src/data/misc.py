from pandas_datareader import data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

my_year_month_fmt = mdates.DateFormatter('%m/%y')


def adj_close():
    start_date = '2000-01-01'
    end_date = '2016-12-31'
    tickers = ['AAPL', 'MSFT', '^GSPC']
    dataSource = 'yahoo'
    panel_data = data.DataReader(tickers, dataSource, start_date, end_date)
    adjClose = panel_data.ix['Close']
    adjClose = adjClose.reindex(pd.date_range(start=start_date, end=end_date, freq='B'))

    return adjClose.fillna(method='ffill')


def log_returns():
    return np.log(adj_close()).diff()


def portfolio_returns():
    r_t = log_returns()
    weights = pd.DataFrame(1 / 3, r_t.index, r_t.columns)
    multiplied = weights.dot(r_t.transpose())

    return pd.Series(np.diag(multiplied), index=r_t.index)


def plot_portfolio_returns():
    port_log_returns = portfolio_returns()
    port_relative_returns = (np.exp(port_log_returns.cumsum()) - 1)

    fig = plt.figure(figsize=[16, 9])
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(port_log_returns.index, port_log_returns.cumsum())
    ax.set_ylabel('Portfolio cumulative log returns')
    ax.grid()

    ax = fig.add_subplot(2, 1, 2)
    ax.plot(port_relative_returns.index, 100 * port_relative_returns)
    ax.set_ylabel('Portfolio total relative returns (%)')
    ax.grid()
    plt.show()


def portfolio_yearly_return():
    close = adj_close()
    days_in_year = 52 * 5
    days_in_data = close.shape[0]
    number_of_years = days_in_data / days_in_year

    total_return = (np.exp(portfolio_returns().cumsum()) - 1)[-1]
    average_yearly_return = (1 + total_return) ** (1 / number_of_years) - 1

    print('Total portfolio return is: ' +
          '{:5.2f}'.format(100 * total_return) + '%')
    print('Average yearly return is: ' +
          '{:5.2f}'.format(100 * average_yearly_return) + '%')


def plot_adj_price():
    adjClose = adj_close()
    msft = adjClose.loc[:, 'ENGI.PA']
    shortRollingMsft = msft.rolling(window=20).mean()
    longRollingMsft = msft.rolling(window=100).mean()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(msft.index, msft, label='MSFT')
    ax.plot(shortRollingMsft.index, shortRollingMsft, label='20 days rolling')
    ax.plot(longRollingMsft.index, longRollingMsft, label='100 days rolling')
    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price ($)')
    ax.legend()
    plt.show()


def plot_returns():
    returns = log_returns()
    fig = plt.figure(figsize=[16, 9])
    ax = fig.add_subplot(2, 1, 1)

    for c in returns:
        ax.plot(returns.index, returns[c].cumsum(), label=str(c))

    ax.set_ylabel('Cummulative returns')
    ax.legend(loc="best")
    ax.grid()

    ax = fig.add_subplot(2, 1, 2)

    for c in returns:
        ax.plot(returns.index, 100 * (np.exp(returns[c].cumsum()) - 1), label=str(c))

    ax.set_ylabel('Relative returns')
    ax.legend(loc="best")
    ax.grid()

    plt.show()


def plot_rolling_averages(span):
    start_date = '2015-01-01'
    end_date = '2016-12-31'

    close = adj_close()
    exp_rolling = close.ewm(span=span, adjust=False).mean()
    rolling = close.rolling(window=span).mean()

    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(close.ix[start_date:end_date, :].index, close.ix[start_date:end_date, 'MSFT'], label='Price')

    ax.plot(exp_rolling.ix[start_date:end_date, :].index, exp_rolling.ix[start_date:end_date, 'MSFT'],
            label='Span 20-days EMA')

    ax.plot(rolling.ix[start_date:end_date, :].index, rolling.ix[start_date:end_date, 'MSFT'], label='20-days SMA')

    ax.legend(loc='best')
    ax.set_ylabel('Price in $')
    ax.grid()
    ax.xaxis.set_major_formatter(my_year_month_fmt)
    plt.show()


def rollin_average_strategy(span):
    close = adj_close()
    exp_rolling = close.ewm(span=span, adjust=False).mean()
    weights = (close - exp_rolling).apply(np.sign()) * 1 / 3
    weights_lagged = weights.shift(1)


if __name__ == '__main__':
    plot_rolling_averages(20)
