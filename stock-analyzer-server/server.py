from flask import Flask
from flask_cors import CORS

from blueprints.strong_stocks import strong_stocks
from blueprints.buy_sell_points import buy_sell_points

app = Flask(__name__)
app.register_blueprint(strong_stocks, url_prefix='/strong_stocks')
app.register_blueprint(buy_sell_points, url_prefix='/buy_sell_points')
CORS(app)


@app.route('/')
def root():
    return 'Server is alive'


if __name__ == '__main__':
    app.run(debug=True)
