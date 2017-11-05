from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

def importData():
    tickers = ['ENGI.PA', 'MSFT', '^GSPC']
    dataSource = 'yahoo'
    startDate = '2000-01-01'
    endDate = '2016-12-31'
    panelData = data.DataReader(tickers, dataSource, startDate, endDate)
    adjClose = panelData.ix['Close']
    adjClose = adjClose.reindex(pd.date_range(start=startDate, end=endDate, freq='B'))
    adjClose = adjClose.fillna(method='ffill')

    return adjClose

def plotData():
    adjClose = importData()
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

if __name__ == '__main__':
    plotData()
    print('hello world')