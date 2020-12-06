import pandas as pd
from stock_pandas import StockDataFrame

from data.utils import Connect


def get_prices(ticker, days):
    sql = """
        SELECT open, high, low, close
        FROM ohlc
        WHERE ticker = '{}'
         ORDER BY DATE Desc
        LIMIT {}
    """.format(ticker, days)
    prices = []
    with Connect() as conn:
        cur = conn.execute(sql)
        for row in cur.fetchall():
            prices.append(row)
    return prices[::-1]


def calc_ma(prices, span=5):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    return list(stock.exec('ma:{}'.format(span)))


def calc_ema(prices, span=5):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    return list(stock.exec('ema:{}'.format(span)))


def calc_macd(prices, fast_period=12, slow_period=26):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    dif = list(stock.exec('macd.dif:{},{}'.format(fast_period, slow_period)))
    dea = list(stock.exec('macd.dea:{},{}'.format(fast_period, slow_period)))
    macd = list(stock.exec('macd.macd:{},{}'.format(fast_period, slow_period)))
    return dif, dea, macd


def calc_boll(prices, period=20, times=2, column='close'):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    boll = list(stock.exec('boll:{},{}'.format(period, column)))
    lower = list(stock.exec('boll.lower:{},{},{}'.format(period, times, column)))
    upper = list(stock.exec('boll.upper:{},{},{}'.format(period, times, column)))
    return boll, lower, upper

