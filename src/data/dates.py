import pandas as pd


def date_parser(date_string):
    return pd.datetime.strptime(date_string, '%Y-%m-%d')
