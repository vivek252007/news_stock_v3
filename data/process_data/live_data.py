import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import yfinance as yf
from process_data.format_data import ProcessData
from data.config import (
    INTRADAY_INTERVAL,
    TIME_PERIOD,
    TIME_FORMAT,
    DEFAULT_TIMEZONE
)


class FetchLiveData:
    def __init__(self, ticker_symbl):
        self.ticket_symbl = ticker_symbl
        self.process_data = ProcessData(
            TIME_FORMAT,
            DEFAULT_TIMEZONE
        )
        self.ticker_data = yf.Ticker(self.ticket_symbl)

    def stock(self):
        raw_stock_data = self.ticker_data.history(
            period=TIME_PERIOD,
            interval=INTRADAY_INTERVAL,
            prepost=True  # download pre/post regular market hours data
        )
        return self.process_data.process_stock_data(raw_stock_data)

    def news(self):
        raw_news_data = self.ticker_data.news
        return self.process_data.process_news_data(raw_news_data)


if __name__ == "__main__":
    data_obj = FetchLiveData("NVDA")
    stock_data = data_obj.stock()
    news_data = data_obj.news()