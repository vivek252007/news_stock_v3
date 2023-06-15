import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import yfinance as yf
from process_data.format_data import ProcessData
from config import (
    INTRADAY_INTERVAL,
    TIME_PERIOD,
    TIME_FORMAT,
    DEFAULT_TIMEZONE,
    NUMBER_OF_TICKER_TO_PROCESS
)
from stock_tickers.get_ticker_list import ticker_symbols


class FetchBatchData:
    def __init__(self):
        self.process_data = ProcessData(
            TIME_FORMAT,
            DEFAULT_TIMEZONE
        )
        self.tickers_data = yf.Tickers(
            ticker_symbols(top_n=NUMBER_OF_TICKER_TO_PROCESS, return_type="str")
        )
        self.ticker_list = ticker_symbols(top_n=NUMBER_OF_TICKER_TO_PROCESS)

    def stock(self):
        raw_stock_data = self.tickers_data.history(
            period=TIME_PERIOD,
            interval=INTRADAY_INTERVAL,
            group_by="ticker",
            prepost=True,  # download pre/post regular market hours data
            threads=True,  # use threads for mass downloading
            ignore_tz=False  # Whether to ignore timezone when aligning ticker data from different timezones.
        )
        return {
            ticker: self.process_data.process_stock_data(raw_stock_data[ticker])
            for ticker in self.ticker_list
        }

    def news(self):
        raw_news_data = self.tickers_data.news()
        return {
            ticker: self.process_data.process_news_data(raw_news_data[ticker])
            for ticker in self.ticker_list
        }


if __name__ == "__main__":
    data_obj = FetchBatchData()
    stock_data = data_obj.stock()
    news_data = data_obj.news()

# a = data_obj.tickers_data.news()
# b = a['AAPL']
#
# for news_metadata in b:
#     news_url = news_metadata["link"]
#     print("News url: ", news_url)
#
# d = {}
# for ticker in data_obj.ticker_list:
#     print(ticker)
#     d[ticker] = data_obj.process_data.process_news_data(a[ticker])
#
# from goose3 import Goose
# import pytz
#
# news_url = "https://finance.yahoo.com/news/apple-set-record-high-ahead-100246034.html"
# for news_metadata in b:
#     news_url = news_metadata["link"]
#     print(news_url)
#     tz = pytz.timezone("America/New_York")
#     article = Goose().extract(url=news_url)
#     print(article)
#     # article.cleaned_text
#     print(article.publish_datetime_utc.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S"))