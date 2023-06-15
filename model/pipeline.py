import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from data.data_api import DataAPI
from define_model import SentimentExtractor


class ModelPipeline():
    def __init__(self):
        self.sentiment_ext = SentimentExtractor()

    def live_stream(self, ticker_symbl):
        get_save_data = DataAPI(ticker_symbl)
        news_data = get_save_data.live_news_data()
        stock_data = get_save_data.live_stock_data()
        return stock_data, self.sentiment_ext.get_sentiment_values(news_data, process_desc=False)

    @staticmethod
    def historical_feed(self, ticker_symbl):
        return DataAPI.historical_stock_data(ticker_symbl), \
            DataAPI.historical_news_data(ticker_symbl)

    @staticmethod
    def historical_predictions(self, ticker_symbl):
        return DataAPI.historical_stock_data(ticker_symbl), \
            DataAPI.historical_prediction_data(ticker_symbl)

    @staticmethod
    def stock_post_processing(stock_df):
        stock_data = stock_df[["date", "close"]].to_dict("list")
        s_date, s_price = stock_data["date"], stock_data["close"]
        return s_date, s_price

    @staticmethod
    def news_post_processing(prediction_df):
        prediction_data = prediction_df[["date", "headline", "link",
                                         "headline_neg_sentiment",
                                         "headline_pos_sentiment"]].to_dict("list")
        n_date, n_head, n_link, n_neg, n_pos = prediction_data["date"], \
            prediction_data["headline"], prediction_data["link"], \
            prediction_data["headline_neg_sentiment"], prediction_data["headline_pos_sentiment"]
        return n_date, n_head, n_link, n_neg, n_pos


if __name__ == "__main__":
    # poetry run python -i model/pipeline.py
    mp = ModelPipeline()
    a, b = mp.live_stream("AAPL")
    # c, d = mp.historical_feed("AAPL")
    # e, f = mp.historical_predictions("AAPL")
# import pickle
# with open("news_data", "wb") as handle:
#     pickle.dump(f, handle)
