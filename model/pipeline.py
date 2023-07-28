import sys
from os import path

parentdir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(parentdir)

from data.data_api import DataAPI
from model.define_model import SentimentExtractor


class ModelPipeline():
    def __init__(self):
        self.sentiment_ext = SentimentExtractor()

    def live_stream(self, ticker_symbl):
        get_save_data = DataAPI(ticker_symbl)
        news_data = get_save_data.live_news_data()
        stock_data = get_save_data.live_stock_data()
        return stock_data, self.sentiment_ext.get_sentiment_values(news_data, process_desc=False)

    @staticmethod
    def historical_feed(ticker_symbl):
        return DataAPI.historical_stock_data(ticker_symbl), \
            DataAPI.historical_news_data(ticker_symbl)

    @staticmethod
    def historical_predictions(ticker_symbl):
        return DataAPI.historical_stock_data(ticker_symbl), \
            DataAPI.historical_prediction_data(ticker_symbl)
    #
    # @staticmethod
    # def stock_post_processing(stock_df):
    #     stock_data = stock_df[["Date_time", "Close"]].to_dict("list")
    #     s_date, s_price = stock_data["Date_time"], stock_data["Close"]
    #     return s_date, s_price
    #
    # @staticmethod
    # def news_post_processing(prediction_df):
    #     prediction_data = prediction_df[["Date_time", "Title", "News_url",
    #                                      "title_negative",
    #                                      "title_positive"]].to_dict("list")
    #     n_date, n_head, n_link, n_neg, n_pos = prediction_data["Date_time"], \
    #         prediction_data["Title"], prediction_data["News_url"], \
    #         prediction_data["title_negative"], prediction_data["title_positive"]
    #     return n_date, n_head, n_link, n_neg, n_pos


if __name__ == "__main__":
    # poetry run python -i model/pipeline.py
    mp = ModelPipeline()
    a, b = mp.live_stream("AAPL")
    c, d = mp.historical_feed("AAPL")
    e, f = mp.historical_predictions("AAPL")
    # e = mp.news_post_processing(b)
    # f = mp.stock_post_processing(a)
# import pickle
# with open("news_data", "wb") as handle:
#     pickle.dump(f, handle)
