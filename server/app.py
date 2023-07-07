import sys
from os import path

parentdir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(parentdir)

from server.layout import dash_layout, update_fig_layout
from process_data import get_processed_data, set_color
import textwrap
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback

from model.pipeline import ModelPipeline


app = Dash(__name__)
app.layout = dash_layout
mp = ModelPipeline()

@callback(Output('live-update-graph', 'figure'),
          Input('interval-component', 'n_intervals'),
          Input("ticker", "value"),
          Input("period", "value"),
          Input("chart_type", "value"),
          )
def display_time_series(n, ticker, period, chart_type):
    stock_df, news_df = mp.live_stream(ticker)
    df, mul_ratio = get_processed_data(stock_df, news_df)
    base_line = stock_df['Close'].astype(float).mean()
    fig = go.Figure()
    update_fig_layout(fig)
    df1 = df[["Date_time", "Close"]].dropna()
    df2 = df[["Date_time", "headline_sentiment", "Title"]].dropna()
    df2["display_text"] = df2[["Title", "headline_sentiment"]] \
        .apply(lambda x:
               "<b>Score: </b>" +
               str(round(x.headline_sentiment / mul_ratio, 2)) +
               "<br>" + "<b>Headline: </b>" +
               textwrap.fill(x.Title, 60).replace("\n", " <br>"),
               axis=1
               )

    fig.add_trace(go.Scatter(x=df1["Date_time"], y=df1["Close"],
                             mode='lines',
                             name='Stock Price'))
    fig.add_hline(y=base_line, opacity=0.3)

    fig.add_trace(go.Bar(x=df2["Date_time"], y=df2["headline_sentiment"],
                         base=base_line,
                         marker=dict(color=list(map(set_color, zip(df2["headline_sentiment"], [mul_ratio]*len(df2))

                                                    ))),
                         width=[500000] * len(df2),
                         name='Sentiment',
                         hoverinfo='text',
                         hovertext=df2["display_text"]))

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
# poetry run python -i server/plotly_example.py
