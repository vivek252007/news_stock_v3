import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

try:
    from data.process_data.live_data import FetchLiveData
except ImportError:
    from process_data.live_data import FetchLiveData

from db_utils.db_handle import DbHandle
from data.process_data.live_data import FetchLiveData
from data.config import DATABASE_PATH, PREDICTION_DATABASE_PATH


class DataAPI:
    def __init__(self, ticker_symbl):
        self.ticker_symbl = ticker_symbl
        self.live_data = FetchLiveData(self.ticker_symbl)

    def live_stock_data(self):
        return self.live_data.stock()

    def live_news_data(self):
        return self.live_data.news()

    @staticmethod
    def historical_news_data(ticker_symbl):
        db_handle = DbHandle(
            ticker_symbl,
            DATABASE_PATH
        )
        news_data = db_handle.get_news_data()

        return news_data

    @staticmethod
    def historical_stock_data(ticker_symbl):
        db_handle = DbHandle(
            ticker_symbl,
            DATABASE_PATH
        )
        stock_data = db_handle.get_stock_data()

        return stock_data

    @staticmethod
    def historical_prediction_data(ticker_symbl):
        db_handle = DbHandle(
            ticker_symbl,
            PREDICTION_DATABASE_PATH
        )
        return db_handle.get_prediction_data()


if __name__ == "__main__":
    #     poetry run python -i data/data_api.py
    get_save_data = DataAPI("AAPL")
    # get_save_data.historical_stock_data()
    # get_save_data.historical_news_data()
    get_save_data.live_news_data()
    get_save_data.live_stock_data()
