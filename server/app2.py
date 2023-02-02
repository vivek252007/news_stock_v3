from flask import Flask, render_template, request
from model.pipeline import ModelPipeline

app = Flask(__name__)

web_page_loc = "main_page.html"


@app.route('/')
def dropdown():
    tickers_list = ['AAPL', 'GOOG', 'NVDA', 'TSLA']
    return render_template(web_page_loc, tickers=tickers_list)


@app.route("/test.py", methods=['GET', 'POST'])
def test():
    select = request.form.get('ticker_select')
    output = str(ModelPipeline().news_post_processing(select))
    return output

@app.route("/username")
@app.route("/username/<name>")
def username(name = "Vivek"):
    return f"<h1> My Name : {name} <h1>"


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)