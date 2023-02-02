import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from db_utils.queries import SqlQueries
import pandas as pd
from db_utils.conn_api import ConnAPI
from config import (
    STOCK_TABLE_COLUMNS,
    NEWS_TABLE_COLUMNS,
    PREDICTION_COLUMNS
)


class DbHandle:
    def __init__(self, ticker, database):
        self.ticker = ticker
        self.db_conn = ConnAPI(database)
        self.sql_queries = SqlQueries(self.ticker)

    def save_stock_data(self, data):
        if self.db_conn is not None:
            # create stock data table and insert data into it.
            self.db_conn.create_table(self.sql_queries.create_stock_table)
            self.db_conn.insert_data(
                self.sql_queries.insert_stock_table,
                data
            )
        else:
            print("Error! cannot insert data into the stock data table")

    def save_news_data(self, data):
        if self.db_conn is not None:
            # create news data table and insert data into it.
            self.db_conn.create_table(self.sql_queries.create_news_table)
            self.db_conn.insert_data(
                self.sql_queries.insert_news_table,
                data
            )
        else:
            print("Error! cannot insert data into the news data table")

    def save_prediction_data(self, data):
        if self.db_conn is not None:
            # create news data table and insert data into it.
            self.db_conn.create_table(self.sql_queries.create_sentiment_table)
            self.db_conn.insert_data(
                self.sql_queries.insert_sentiment_table,
                data
            )
        else:
            print("Error! cannot insert data into the news data table")

    def get_stock_data(self, return_df=True):
        if self.db_conn is not None:
            data = self.db_conn.get_data(self.sql_queries.get_stock_data_query)
            return pd.DataFrame(
                data,
                columns=STOCK_TABLE_COLUMNS
            ) if return_df else data
        else:
            print("Error! cannot retrieve data from the stock data table")

    def get_news_data(self, return_df=True):
        if self.db_conn is not None:
            data = self.db_conn.get_data(self.sql_queries.get_news_data_query)
            return pd.DataFrame(
                data,
                columns=NEWS_TABLE_COLUMNS
            ) if return_df else data
        else:
            print("Error! cannot retrieve data from the news data table")

    # TODO: to_pandas_df and to_nested_list functions needed.
    def get_prediction_data(self, return_df=True):
        if self.db_conn is not None:
            data = self.db_conn.get_data(self.sql_queries.get_sentiment_data_query)
            return pd.DataFrame(
                data,
                columns=NEWS_TABLE_COLUMNS + PREDICTION_COLUMNS
            ) if return_df else data
        else:
            print("Error! cannot retrieve data from the news data table")


if __name__ == '__main__':
    db = DbHandle("GOOG", r"data/database/news_data.db")
    db.save_stock_data([("2", "1", "1", "1", "1", "1"), ("3", "1", "1", "1", "1", "1")])
    stock_data = db.get_stock_data()
    db.save_news_data([("2", "1", "1", "1"), ("3", "1", "1", "2")])
    news_data = db.get_news_data()
