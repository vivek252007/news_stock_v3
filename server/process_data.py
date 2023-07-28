import pandas as pd
import textwrap


def set_color(data):
    x, mul_ratio = data
    if x > mul_ratio / 2:
        return "#109618"
    elif 0 <= x <= mul_ratio / 2:
        return "#B6E880"
    elif -mul_ratio / 2 <= x <= 0:
        return "#FFA15A"
    elif x < -mul_ratio / 2:
        return "#D62728"
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

    df1 = df[["Date_time", "Close"]].dropna()
    df2 = df[["Date_time", "headline_sentiment", "Title", "News_url"]].dropna()
    df2["display_text"] = df2[["Title", "News_url", "headline_sentiment"]] \
        .apply(lambda x:
               "<b>Score: </b>" +
               str(round(x.headline_sentiment / mul_ratio, 2)) +
               "<br>" + "<b>Headline: </b>" +
               textwrap.fill(x.Title, 60).replace("\n", " <br>") +
               "<br>" + "<b>News Url: </b>" + f"<a href=\"{x.News_url}\">{x.News_url}</a>",
               axis=1
               )
    return df1, df2, mul_ratio, stock_df['Close'].astype(float).mean()


def get_data(mp, chart_type, ticker):
    if chart_type == "Historical":
        col_renamed = {"Title_neg_senti": "title_negative",
                       "Title_pos_senti": "title_positive"
                       }
        stock_df, news_df = mp.historical_predictions(ticker)
        news_df = news_df.rename(columns=col_renamed)
    elif chart_type == "Live":
        stock_df, news_df = mp.live_stream(ticker)
    else:
        print("Unknown Chart Type")
    return stock_df, news_df


# a, b = mp.live_stream("MMM")
# c, d = mp.historical_feed("MMM")
# Add Twitter feed to improve
# Add bollinger bands to improve
