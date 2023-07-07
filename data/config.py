

TICKER_PATH = "data/stock_tickers/sp_500_with_sector.csv"
NUMBER_OF_TICKER_TO_PROCESS = 20
DATABASE_PATH = r"data/dbs/news_data.db"
PREDICTION_DATABASE_PATH = r"data/dbs/model_predictions.db"
INTRADAY_INTERVAL = "1m"
TIME_PERIOD = "1d"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_TIMEZONE = "America/New_York"

NEWS_TABLE_COLUMNS = ['Date_time',
                      'Title',
                      'Text',
                      'News_url',
                      'Related_tickers',
                      'Publisher',
                      'News_type',
                      'Timezone']


STOCK_TABLE_COLUMNS = ['Date_time',
                       'Open',
                       'High',
                       'Low',
                       'Close',
                       'Volume',
                       'Dividends',
                       'Stock_splits',
                       'Timezone']

PREDICTION_COLUMNS = ['Date_time',
                      'Title',
                      'Text',
                      'News_url',
                      'Title_neg_senti',
                      'Title_pos_senti',
                      'Text_neg_senti',
                      'Text_pos_senti']

# https://stockmarketmba.com/stocksinthesp500.php
# https://github.com/gargankush/SP500_Stock_List/blob/main/S%26P500Tickers.csv
# import pandas as pd
# a = pd.read_csv("data/stock_tickers/sp_500.csv")
# ticker_list = pd.read_html(
#     'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# df = ticker_list[0]
#
# c= pd.merge(a, df.drop(columns=["GICS Sector"]), on="Symbol", how="left")
# c.to_csv("data/stock_tickers/sp_500_with_sector.csv")
#