import pandas as pd


def set_color(data):
    x, mul_ratio = data
    if x > mul_ratio / 2:
        return "green"
    elif 0 <= x <= mul_ratio / 2:
        return "lightgreen"
    elif -mul_ratio / 2 <= x <= 0:
        return "red"
    elif x < -mul_ratio / 2:
        return "darkred"
    else:
        return "white"


def get_processed_data(stock_df, news_df):
    col_mean = stock_df['Close'].astype(float).mean()
    stock_close = stock_df['Close'].astype(float)
    mul_ratio = stock_close.max() - stock_close.min()
    news_df["headline_sentiment"] = (news_df["title_positive"] + news_df["title_negative"]) * (mul_ratio)
    news_df['label'] = news_df['headline_sentiment'] \
        .apply(lambda x: "Positive Sentiment" if float(x) > col_mean else "Negative Sentiment")
    df = pd.merge(stock_df, news_df, how="outer", on="Date_time").sort_values(by="Date_time", axis=0).reset_index(
        drop=True)
    df[['Open', 'Close', 'High', 'Low', 'Volume']] = df[['Open', 'Close', 'High', 'Low', 'Volume']].astype(
        float).fillna(
        method="bfill")
    df['label'] = df['label'].fillna("Negative Sentiment")
    return df, mul_ratio

# a, b = mp.live_stream("MMM")
# c, d = mp.historical_feed("MMM")
# Add Twitter feed to improve
# Add bollinger bands to improve
