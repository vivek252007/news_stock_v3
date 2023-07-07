# ================================================================================
# https://discourse.bokeh.org/t/how-do-i-make-omit-missing-dates-gaps-in-graph-when-using-datetime-as-x-axis/3712/2#
# https://medium.com/@n.j.marey/my-experience-with-flask-and-bokeh-plus-a-small-tutorial-7b49b2e38c76
import pickle
import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, OpenURL, TapTool, Span, Legend, LegendItem
from bokeh.palettes import RdYlGn as color_map
from bokeh.transform import linear_cmap
from bokeh.layouts import column, row
from model.pipeline import ModelPipeline


pd.set_option('display.max_rows', None)


def get_processed_data(stock_df, news_df):
    col_mean = stock_df['close'].astype(float).mean()
    news_df["pos_sentiment"] = news_df["headline_pos_sentiment"]
    news_df["neg_sentiment"] = news_df["headline_neg_sentiment"]
    news_df["headline_sentiment"] = news_df["pos_sentiment"] + news_df["neg_sentiment"] + col_mean
    news_df['label'] = news_df['headline_sentiment'] \
        .apply(lambda x: "Positive Sentiment" if float(x) > col_mean else "Negative Sentiment")

    df = pd.merge(stock_df, news_df, how="outer", on="date").sort_values(by="date", axis=0).reset_index(drop=True)
    df[['open', 'close', 'high', 'low', 'volume']] = df[['open', 'close', 'high', 'low', 'volume']].fillna(
        method="bfill")
    df['label'] = df['label'].fillna("Negative Sentiment")

    axis_override = {
        i: date.strftime('%d %b') for i, date in enumerate(pd.to_datetime(df["date"]))
    }
    return ColumnDataSource(df), col_mean, axis_override


def plot_obj(source, vbar_mean, x_axis_override):
    x_axis_col = "index"

    palette = tuple(reversed(color_map[11]))
    colormapper = linear_cmap(
        field_name="headline_sentiment",
        palette=palette,
        low=vbar_mean - 1,
        high=vbar_mean + 1
    )

    TOOLS = "crosshair,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,tap,save"

    p = figure(
        width=1000,
        height=500,
        title="Stock Price with Sentiment",
        x_axis_label="Timeline",
        y_axis_label="Price",
        # sizing_mode='scale_width',
        tools=TOOLS)

    p.background_fill_color = "beige"
    p.xaxis.major_label_overrides = x_axis_override
    hline = Span(
        location=vbar_mean,
        dimension='width',
        line_color='black',
        line_width=1
    )

    # add multiple renderers
    p1 = p.line(
        x_axis_col,
        "close",
        legend_label="Closing Price",
        color="navy",
        line_width=2,
        source=source
    )
    p2 = p.vbar(
        x=x_axis_col,
        width=1,
        top="headline_sentiment",
        bottom=vbar_mean,
        legend_field="label",
        color=colormapper,
        fill_alpha=0.4,
        line_width=0.5,
        source=source
    )

    hover_tool_1 = HoverTool(
        renderers=[p1],
        tooltips=[
            ('Time', '@date{%T}'),
            ('Open', '$@open{0.00 a}'),
            ('Close', '$@close{0.00 a}'),
            ('High', '$@high{0.00 a}'),
            ('Low', '$@low{0.00 a}'),
            ('Volume', '@volume{0.00 a}')
        ],
        formatters={
            '@date': 'datetime',
            '@{close}': 'numeral',
        },
        mode='vline'
    )

    hover_tool_2 = HoverTool(
        renderers=[p2],
        tooltips=[
            ('Time', '@date{%T}'),
            ('Headline', '@headline'),
            ('Positive', '@headline_pos_sentiment{0.00 a}'),
            ('Negative', '@headline_neg_sentiment{0.00 a}')
        ],
        formatters={
            '@date': 'datetime',
        },
        mode='vline'
    )

    url = "@link"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)
    p.renderers.extend([hline])
    p.add_tools(hover_tool_1)
    p.add_tools(hover_tool_2)
    output_file("custom_datetime_axis.html", title="custom_datetime_axis.py example")
    return p


stock_file = "stock_data"
news_file = "news_data"
with open(stock_file, "rb") as handle:
    stock_df = pickle.load(handle)

with open(news_file, "rb") as handle:
    news_df = pickle.load(handle)

source, vbar_mean, x_axis_override = get_processed_data(stock_df, news_df)
plot = plot_obj(source, vbar_mean, x_axis_override)
from bokeh.models import Dropdown

menu = pd.read_csv("../../data/stock_tickers/sp_500_with_sector.csv")[["Description", "Symbol"]][:10].to_dict("split")["data"]
# menu = [("Item 1", "item_1"), ("Item 2", "item_2"), ("Item 3", "item_3")]

dropdown = Dropdown(label="Select Stock", button_type="warning", menu=menu)


def handler(event):
    mp = ModelPipeline()
    # a, b = mp.live_stream("MMM")
    # c, d = mp.historical_feed("MMM")
    stock_df, news_df = mp.historical_predictions(event.item)
    source, vbar_mean, x_axis_override = get_processed_data(stock_df, news_df)
    plot = plot_obj(source, vbar_mean, x_axis_override)
    layout = row(
        column(dropdown),
        plot,
    )
    show(layout)

dropdown.on_click(handler)

layout = row(
    column(dropdown),
    plot,
)

show(layout)
# show(p)
