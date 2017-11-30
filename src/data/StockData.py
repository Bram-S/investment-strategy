import os
import settings
import pandas as pd
import src.data.dates as dates


class StockData:
    date_column = 'Date'

    def __init__(self, market_code, ticker):
        self.ticker = ticker
        self.market_code = market_code
        self.path = os.path.join(settings.RESOURCES_ROOT, market_code, ticker + '.csv')
        self.data = self.load_data_csv()

    def load_data_csv(self):
        return pd.read_csv(self.path, index_col=self.date_column, parse_dates=[self.date_column],
                           date_parser=dates.date_parser)

    def end_date(self):
        return self.data.index[-1].date()


if __name__ == '__main__':
    data = StockData('BR', 'VALOR')
    print(data.end_date())
