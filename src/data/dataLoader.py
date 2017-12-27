import pandas as pd
import src.data.dates as dates


def load_data_csv(path, date_column):
    return pd.read_csv(path, index_col=date_column, parse_dates=[date_column], date_parser=dates.date_parser)
