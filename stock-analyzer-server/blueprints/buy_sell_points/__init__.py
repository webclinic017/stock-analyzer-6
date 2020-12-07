from flask import Blueprint, jsonify

from data.db import Connect

buy_sell_points = Blueprint('buy_sell_points', __name__)


@buy_sell_points.route('/')
def index():
    sql = """
        SELECT *
        FROM buy_sell
    """
    data = []
    keys = ['id', 'name', 'price', 'changeRate', 'bollRel1D', 'volume']
    with Connect() as conn:
        cur = conn.execute(sql)
        for row in cur.fetchall():
            data.append(dict(zip(keys, row)))
    return jsonify(data)
