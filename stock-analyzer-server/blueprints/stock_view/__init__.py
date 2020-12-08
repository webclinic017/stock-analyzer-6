from flask import Blueprint, jsonify, request

from data.db import Connect

stock_view = Blueprint('stock_view', __name__)
from data.analyzer.utils import get_ticker_name


@stock_view.route('/get_ohlc')
def index():
    ticker = str(request.args.get('id'))
    with Connect() as conn:
        sql = """
            select date, open, high, low, close, volume
            from ohlc
            where ticker = '{}'
            order by date asc
        """.format(ticker)
        cur = conn.execute(sql)
        data = cur.fetchall()
    return jsonify({'data': data, 'name': get_ticker_name(ticker)})
