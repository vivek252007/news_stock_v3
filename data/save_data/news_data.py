import sys
from time import sleep
from os import path

parentdir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(parentdir)
# sys.path.append(os.path.join(parentdir, "data"))
# sys.path.append(os.path.join(parentdir, "model"))
# sys.path.append(os.path.join(parentdir, "server"))

from data.db_utils.db_handle import DbHandle
from data.config import DATABASE_PATH
from data.process_data.batch_data import FetchBatchData


class SaveNewsData:
    def __init__(self):
        self.batch_data = FetchBatchData()

    def save_news_data(self):
        try:
            while True:
                for ticker, news in self.batch_data.news().items():
                    print("###########\n" + ticker + " News")
                    print(f"News Articles Count: {len(news)}")
                    db_handler = DbHandle(ticker, DATABASE_PATH)
                    db_handler.save_news_data(news.to_dict("split")["data"])
                sleep(900)

        except Exception as e:
            print(f"Save News Data for {ticker}: {e}")
            self.handle_crash()

    def handle_crash(self):
        sleep(60)  # restart after 60 secs
        self.save_news_data()


if __name__ == "__main__":
    # poetry run python -i data/save_data/news_data.py
    save_data = SaveNewsData()
    save_data.save_news_data()