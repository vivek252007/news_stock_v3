import sys
from time import sleep
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from data.db_utils.db_handle import DbHandle
from data.config import DATABASE_PATH
from data.process_data.batch_data import FetchBatchData


class SaveStockData:
    def __init__(self):
        self.batch_data = FetchBatchData()

    def save_stock_data(self):
        try:
            while True:
                for ticker, stock in self.batch_data.stock().items():
                    print("###########\n" + ticker + " Stock")
                    print(f"Stock Prices: {stock['Date_time'].iloc[0]} - {stock['Date_time'].iloc[-1]}")
                    db_handler = DbHandle(ticker, DATABASE_PATH)
                    db_handler.save_stock_data(stock.to_dict("split")["data"])
                sleep(180)

        except Exception as e:
            print(f"Save Stock Data: {e}")
            self.handle_crash()

    def handle_crash(self):
        sleep(60)  # restart after 60 secs
        self.save_stock_data()


if __name__ == "__main__":
    # poetry run python -i data/stock_data.py
    save_data = SaveStockData()
    save_data.save_stock_data()