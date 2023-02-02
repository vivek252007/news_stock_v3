import plotly.express as px
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

from model.pipeline import ModelPipeline

# Add Twitter feed to improve
# Add bollinger bands to improve
def get_processed_data(stock_df, news_df):
    col_mean = stock_df['close'].astype(float).mean()
    news_df["pos_sentiment"] = news_df["headline_pos_sentiment"]
    news_df["neg_sentiment"] = news_df["headline_neg_sentiment"]
    news_df["headline_sentiment"] = news_df["pos_sentiment"] + news_df["neg_sentiment"] + col_mean
    news_df['label'] = news_df['headline_sentiment'] \
        .apply(lambda x: "Positive Sentiment" if float(x) > col_mean else "Negative Sentiment")

    df = pd.merge(stock_df, news_df, how="outer", on="date").sort_values(by="date", axis=0).reset_index(drop=True)
    df[['open', 'close', 'high', 'low', 'volume']] = df[['open', 'close', 'high', 'low', 'volume']].astype(
        float).fillna(
        method="bfill")
    df['label'] = df['label'].fillna("Negative Sentiment")

    return df


app = Dash(__name__)


app.layout = html.Div([
    html.H4('Sentiment Analysis'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select stock:"),
    dcc.Dropdown(
        id="ticker",
        options=["AAPL", "GOOG", "MSFT"],
        value="AAPL",
        clearable=False,
    ),
])

mp = ModelPipeline()
# a, b = mp.live_stream("MMM")
# c, d = mp.historical_feed("MMM")

@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"))
def display_time_series(ticker):
    stock_df, news_df = mp.historical_predictions(ticker)
    df = get_processed_data(stock_df, news_df)
    fig = px.line(df, x='date', y="close")
    return fig


# fig.update_layout(
#     autosize=True,
#     # width=500,
#     height=500,
#     margin=dict(
#         l=50,
#         r=50,
#         b=100,
#         t=100,
#         pad=4
#     ),
#     paper_bgcolor="LightSteelBlue",
# )

app.run_server(debug=True)
# poetry run python -i server/plotly_example.py
