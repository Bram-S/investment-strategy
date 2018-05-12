import os
import settings
import pandas as pd
import json


def read_all_stock_names(market_code):
    with open(os.path.join(settings.RESOURCES_ROOT, market_code, 'config.json')) as config:
        config = json.load(config)

    stocks_file = config['all_stocks_file']
    separator = config['separator']
    market_name = config['market_name']
    path = os.path.join(settings.RESOURCES_ROOT, stocks_file)
    stock_names_data = pd.read_csv(path, sep=separator)

    return stock_names_data[stock_names_data['Market'].str.startswith(market_name)]['Symbol']


if __name__ == '__main__':
    print(read_all_stock_names('XAMS'))
