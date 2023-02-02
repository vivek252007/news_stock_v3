import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from data.data_api import GetData
from .define_model import SentimentExtractor


class ModelPipeline():
    def __init__(self):
        self.get_save_data = GetData()
        self.sentiment_ext = SentimentExtractor()

    def live_stream(self, ticker_symbl):
        stock_data, news_data = self.get_save_data.live_ticker_data(ticker_symbl)
        return stock_data, self.sentiment_ext.get_sentiment_values(news_data, process_desc=False)

    def historical_feed(self, ticker_symbl):
        return self.get_save_data.historical_stock_data(ticker_symbl), \
            self.get_save_data.historical_news_data(ticker_symbl)

    def historical_predictions(self, ticker_symbl):
        return self.get_save_data.historical_stock_data(ticker_symbl), \
            self.get_save_data.historical_prediction_data(ticker_symbl)

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
    # a, b = mp.live_stream("MMM")
    # c, d = mp.historical_feed("MMM")
    e, f = mp.historical_predictions("AAPL")
# import pickle
# with open("news_data", "wb") as handle:
#     pickle.dump(f, handle)
