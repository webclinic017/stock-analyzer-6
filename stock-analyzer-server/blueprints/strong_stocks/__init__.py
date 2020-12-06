from flask import Blueprint, jsonify

from data.utils import Connect

strong_stocks = Blueprint('strong_stocks', __name__)


@strong_stocks.route('/')
def index():
    sql = """
        SELECT *
        FROM strong_stocks
    """
    data = []
    keys = ['id', 'name', 'price', 'change', 'changeRate', 'rel1D', 'rel5D', 'rel20D', 'cs', 'sm', 'ml', 'volume']
    with Connect() as conn:
        cur = conn.execute(sql)
        for row in cur.fetchall():
            data.append(dict(zip(keys, row)))
    return jsonify(data)
