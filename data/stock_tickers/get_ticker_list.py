import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import pandas as pd
from config import TICKER_PATH


def ticker_symbols(top_n=500, return_type="list"):
    ticker_list = list(pd.read_csv(TICKER_PATH)["Symbol"])[:top_n]
    if return_type == "list":
        return ticker_list
    elif return_type == "str":
        tickers_str = ""
        for ticker in ticker_list:
            tickers_str += ticker + " "
        return tickers_str.strip(" ")
