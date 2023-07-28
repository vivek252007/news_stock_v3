from dash import dcc, html
import pandas as pd
import re

ticker_list = [{'label': name, 'value': ticker}
               for ticker, name in list(
        pd.read_csv("data/stock_tickers/sp_500_with_sector.csv")[["Symbol", "Description"]]
        .head(20)
        .apply(lambda x: (x.Symbol, re.sub(' +', ' ', re.sub("Inc\.?", "",x.Description.replace("Class", "").strip()))), axis=1)
    )]

div_style = {'font-family': 'Courier New',
             'width': '400px',
             'display': 'table-cell',
             'padding': '10px'}

dash_layout = html.Div([
    html.H1('Sentiment Analysis', style={'font-family': 'Verdana', 'color': 'SlateBlue'}),

    html.Div(
        [
            html.H4("Stock", style={'margin-right': '2em'}),
            dcc.Dropdown(
                id="ticker",
                options=ticker_list,
                value="AAPL",
                clearable=False,
                style=dict(
                    width='150px',
                )
            )
        ],
        style=div_style
    ),
    html.Div(
        [
            html.H4("Chart Type", style={'margin-right': '2em'}),
            dcc.RadioItems(
                id="chart_type",
                options=["Live", "Historical"],
                value="Live",
            )
        ],
        style=div_style
    ),
    html.Div(
        [
            html.H4("Period", style={'margin-right': '2em'}),
            dcc.Dropdown(
                id="period",
                options=[
                    {'label': '1 Day', 'value': '1d'},
                    {'label': '2 Day', 'value': '2d'},
                    {'label': '5 Day', 'value': '5d'},
                    {'label': '7 Day', 'value': '7d'}
                ],
                value="1d",
                clearable=False,
                style=dict(
                    width='100px',
                )
            )
        ],
        style=div_style
    ),
    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Graph(id="live-update-graph"),
]
)


def update_fig_layout(fig):
    fig.update_layout(
        title="<b>Stock With Sentiment<b>",
        xaxis_title="<b>Time<b>",
        yaxis_title="<b>Stock Price<b>",
        legend_title="<b>Legend<b>",
        height=700,
        hovermode="x unified",
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        ),
        uirevision=True
    )
    return fig
