import sys
from os import path, environ

parentdir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(parentdir)

from server.layout import dash_layout, update_fig_layout
from process_data import get_processed_data, set_color, get_data
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, ctx
from plotly.subplots import make_subplots
import webbrowser

from model.pipeline import ModelPipeline
environ["TOKENIZERS_PARALLELISM"] = "false"

app = Dash(__name__)
fig = go.Figure(layout=go.Layout(clickmode='event+select'))
app.layout = dash_layout
mp = ModelPipeline()


@callback(Output('live-update-graph', 'figure'),
          Input('interval-component', 'n_intervals'),
          Input("ticker", "value"),
          Input("chart_type", "value"),
          Input("period", "value"),
          Input('live-update-graph', 'clickData')
          )
def display_time_series(n, ticker, chart_type, period, clickData):
    print("Trigger: ", ctx.triggered_id)
    # if ctx.triggered_id in ("interval-component", "ticker", "chart_type", "period"):
    if ctx.triggered_id == "live-update-graph":
        # print(clickData)
        try:
            url = clickData['points'][1]['customdata']
            webbrowser.open_new_tab(url)
            # ctx.inputs_list[-1] = {'id': 'live-update-graph', 'property': 'clickData'}
        except:
            pass
    else:
        stock_df, news_df = get_data(mp, chart_type, ticker)
        line_df, bar_df, mul_ratio, base_line = get_processed_data(stock_df, news_df)
        # fig = go.Figure(layout=go.Layout(clickmode='event+select'))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        update_fig_layout(fig)
        fig.add_trace(go.Scatter(x=line_df["Date_time"], y=line_df["Close"],
                                 mode='lines',
                                 name='Stock Price'), )
        fig.add_hline(y=base_line, opacity=0.3)

        fig.add_trace(go.Bar(x=bar_df["Date_time"], y=bar_df["headline_sentiment"],
                             customdata=list(bar_df["News_url"]),
                             base=base_line,
                             marker=dict(
                                 color=list(map(set_color, zip(bar_df["headline_sentiment"], [mul_ratio] * len(bar_df))))
                             ),
                             opacity=1.0,

                             width=[10000000] * len(bar_df) if chart_type == "Historical" else [500000] * len(bar_df),
                             name='Sentiment',
                             hoverinfo='text',
                             hovertext=bar_df["display_text"]))

        dash_layout.to_plotly_json()["props"]["children"][-1].figure = fig
        return fig
    # else:
    #     print(f"Not a valid trigger: {ctx.triggered_id}")


if __name__ == "__main__":
    app.run_server(debug=True)
# poetry run python -i server/app.py
