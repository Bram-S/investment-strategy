import os
import settings
import src.data.dataLoader as dataLoader


class StockActions:
    date_column = 'Date'
    path_root = 'actions'

    def __init__(self, market_code, ticker):
        self.ticker = ticker
        self.market_code = market_code
        # TODO this path is used in Market and here => should set somewhere central
        self.path = os.path.join(settings.RESOURCES_ROOT, market_code, self.path_root, ticker + '.csv')
        csv_data = dataLoader.load_data_csv(self.path, self.date_column)
        self.data = csv_data[~csv_data.index.duplicated()]

    def end_date(self):
        return self.data.index[-1].date()
