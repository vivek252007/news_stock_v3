from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf

app = Flask(__name__)


# Define the root route
@app.route('/')
def index():
    return render_template('index3.html')


@app.route('/callback/<endpoint>')
def cb(endpoint):
    if endpoint == "getStock":
        return gm(request.args.get('data'), request.args.get('period'), request.args.get('interval'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = yf.Ticker(stock)
        return json.dumps(st.info)
    else:
        return "Bad endpoint", 400


# Return the JSON data for the Plotly graph
def gm(stock, period, interval):
    st = yf.Ticker("AAPL")
    # Create a line graph
    df = st.history(period="10d", interval="1m")
    df = df.reset_index()
    df.columns = ['Date-Time'] + list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
                  hover_data=("Open", "Close", "Volume"),
                  range_y=(min, max), template="seaborn")

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
'''
# thisTCIN=`basename "$thisImage"`;thisTCIN=${thisTCIN%%.*};thisTCIN=${thisTCIN%%_*}
convert "test.py.webp" -quiet -strip -background white -alpha off -flatten -resize '500x500' "test_small.gif"
convert "test_small.gif" \( +clone -fx 'p{0,0}' \) -compose Difference -composite -modulate 100,0 -alpha off "test_diff.gif"
convert "test_diff.gif" -threshold 1% "test_threshold_mask.gif"
convert "test_small.gif" "test_threshold_mask.gif" -alpha Off -compose CopyOpacity -composite "test_alpha.gif"
rgb=$(convert "test_alpha.gif" -scale 1x1\! -format '%[fx:int(255*r+.5)],%[fx:int(255*g+.5)],%[fx:int(255*b+.5)]' info:-)
convert -quiet "test_small.gif" -fuzz 10% -fill rgb\("$rgb"\) -opaque white -gravity Center -crop 64x64+0+0 -scale 40x40 "test_swatch.jpg"

'''