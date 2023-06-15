class SqlQueries:
    def __init__(self, ticker):
        self.ticker = ticker
        self._stock_data_queries()
        self._news_data_queries()
        self._sentiment_data_queries()

    def _stock_data_queries(self):
        self.create_stock_table = f'''CREATE TABLE IF NOT EXISTS {self.ticker}_stock (
                                            Date_time text PRIMARY KEY,
                                            Open text,
                                            High text,
                                            Low text,
                                            Close text,
                                            Volume text,
                                            Dividends text,
                                            Stock_splits text,
                                            Timezone text
                                      ); '''

        self.insert_stock_table = f'''INSERT OR REPLACE INTO {self.ticker}_stock VALUES(?,?,?,?,?,?,?,?,?)'''

        self.get_stock_data_query = f"SELECT * FROM {self.ticker}_stock"

    def _news_data_queries(self):
        self.create_news_table = f'''CREATE TABLE IF NOT EXISTS {self.ticker}_news (
                                                Date_time text NOT NULL,
                                                Title text,
                                                Text text,
                                                News_url text PRIMARY KEY,
                                                Related_tickers text,
                                                Publisher text,
                                                News_type text,
                                                Timezone text
                                            ); '''

        self.insert_news_table = f'''INSERT OR REPLACE INTO {self.ticker}_news VALUES(?,?,?,?,?,?,?,?)'''

        self.get_news_data_query = f'''SELECT * FROM {self.ticker}_news'''

    def _sentiment_data_queries(self):
        self.create_sentiment_table = f'''CREATE TABLE IF NOT EXISTS {self.ticker}_sentiment (
                                                Date_time text NOT NULL,
                                                Title text,
                                                Text text,
                                                News_url text PRIMARY KEY,
                                                Title_neg_senti REAL,
                                                Title_pos_senti REAL,
                                                Text_neg_senti REAL,
                                                Text_pos_senti REAL
                                            ); '''

        self.insert_sentiment_table = f'''INSERT OR REPLACE INTO {self.ticker}_sentiment VALUES(?,?,?,?,?,?,?,?)'''

        self.get_sentiment_data_query = f'''SELECT * FROM {self.ticker}_sentiment'''
