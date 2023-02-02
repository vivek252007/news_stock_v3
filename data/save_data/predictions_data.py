import sys
from time import sleep
from os import path
import pandas as pd
from tqdm import tqdm

tqdm.pandas()
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from data.db_utils.db_handle import DbHandle
from model.define_model import SentimentExtractor
from data.config import PREDICTION_DATABASE_PATH, DATABASE_PATH
from data.stock_tickers.get_ticker_list import ticker_symbols


class GetSavePredictions:
    def __init__(self):
        self.sentiment_ext = SentimentExtractor()
        self.ticker_list = ticker_symbols()

    def _process_new_news(self, data_db_handle, pred_db_handle):
        hist_news_df = data_db_handle.process_news_data()

        try:
            processed_news_df = pred_db_handle.get_prediction_data()[["link"]]
            unprocessed_news_df = pd.concat([hist_news_df, processed_news_df]) \
                .drop_duplicates(subset=["link"], keep=False)
        except Exception as e:
            unprocessed_news_df = hist_news_df
            print(f"Process new News: {e}")

        hist_news_with_sentiment = self.sentiment_ext.get_sentiment_values(unprocessed_news_df)
        return hist_news_with_sentiment

    def save_prediction_data(self):
        try:
            while True:
                for company_ticker in self.ticker_list:
                    print("########################\n" + company_ticker + " Prediction Started")

                    db_handler = DbHandle(company_ticker, DATABASE_PATH)
                    pred_db_handler = DbHandle(company_ticker, PREDICTION_DATABASE_PATH)
                    model_predictions = self._process_new_news(db_handler, pred_db_handler)
                    pred_db_handler.save_prediction_data(model_predictions.to_dict("split")["data"])

                    print(company_ticker + " Prediction Completed\n########################\n\n")

        except Exception as e:
            print(f"Save Predictions: {e}")
            self.handle_crash()

    def handle_crash(self):
        sleep(60)  # restart after 60 secs
        self.save_prediction_data()


if __name__ == "__main__":
    # poetry run python -i data/predictions_data.py
    get_save_data = GetSavePredictions()
    get_save_data.save_prediction_data()

