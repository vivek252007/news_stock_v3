#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from goose3 import Goose
import pytz
import pandas as pd
from config import NEWS_TABLE_COLUMNS, STOCK_TABLE_COLUMNS

pd.options.mode.chained_assignment = None #SettingWithCopyWarning

class ProcessData:
    def __init__(self,
                 time_format,
                 default_timezone,
                 ):
        self.time_format = time_format
        self.default_timezone = default_timezone
        self.url_parser = Goose()

    def process_news_text(self, news_url):
        tz = pytz.timezone(self.default_timezone)
        article = self.url_parser.extract(url=news_url)
        return article.cleaned_text, \
            article.publish_datetime_utc.astimezone(tz).strftime(self.time_format)

    def process_news_data(self, raw_news):
        news_list = []
        try:
            for news_metadata in raw_news:
                news_url = news_metadata["link"]
                text, date_time = self.process_news_text(news_url)
                title = news_metadata["title"]
                related_tickers = news_metadata["relatedTickers"]
                publisher = news_metadata["publisher"]
                news_type = news_metadata["type"]
                news_list.append((date_time,
                                  title,
                                  text,
                                  news_url,
                                  related_tickers,
                                  publisher,
                                  news_type,
                                  self.default_timezone
                                  ))
        except Exception as e:
            print(f"News Exception: {e}")
        reversed_data = news_list[::-1] if news_list else news_list
        return pd.DataFrame(
            reversed_data,
            columns=NEWS_TABLE_COLUMNS
        ).astype(str)

    def process_stock_data(self, raw_stock_data):
        raw_stock_data.reset_index(inplace=True)

        raw_stock_data["Date_time"] = raw_stock_data["Datetime"] \
            .apply(lambda x: x.strftime(self.time_format))

        raw_stock_data["Timezone"] = raw_stock_data["Datetime"] \
            .apply(lambda x: x.tz.zone)

        return raw_stock_data \
            .rename(columns={'Stock Splits': 'Stock_splits'}) \
            [STOCK_TABLE_COLUMNS].astype(str)


if __name__ == "__main__":
    data_obj = ProcessData("%Y-%m-%d %H:%M:%S", 'America/New_York')
    news_data = data_obj.process_news_data()
    stock_data = data_obj.process_stock_data()
