import pandas as pd
from stock_pandas import StockDataFrame

from data.tickers import get_stock_hk_spot
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


def get_last_price(ticker):
    return get_prices(ticker, 1)[0][3]


def get_price_change(ticker):
    prices = [p[3] for p in get_prices(ticker, 2)]
    return prices[1] - prices[0], (prices[1] / prices[0] - 1) * 100


def get_ticker_name(ticker):
    sql = """
        SELECT name
        FROM stock_info
        WHERE ticker = '{}'
    """.format(ticker)
    name = ''
    with Connect() as conn:
        cur = conn.execute(sql)
        for row in cur.fetchone():
            name = row
    return name


def get_ticker_volume(ticker):
    df = get_stock_hk_spot()
    return float(list(df[df.symbol == '0{}'.format(ticker[:4])]['amount'])[0])


def calc_ma(prices, span=5):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    return list(stock.exec('ma:{}'.format(span)))


def calc_ema(prices, span=5):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    return list(stock.exec('ema:{}'.format(span)))


def calc_macd(prices):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    dif = list(stock.exec('macd.dif'))
    dea = list(stock.exec('macd.dea'))
    macd = list(stock.exec('macd.macd'))
    return dif, dea, macd


def calc_boll(prices):
    df = pd.DataFrame(prices, columns=['open', 'high', 'low', 'close'])
    stock = StockDataFrame(df)
    boll = list(stock.exec('boll'))
    lower = list(stock.exec('boll.lower'))
    upper = list(stock.exec('boll.upper'))
    return boll, lower, upper


if __name__ == '__main__':
    ticker = '3690.HK'
    prices = get_prices(ticker, 300)
    print(calc_ma(prices)[::-1])
    print(calc_ema(prices, 120)[::-1])
    print(calc_ema(prices, 60)[::-1])
    print(calc_macd(prices)[-1][::-1])
    print(calc_boll(prices)[0][::-1])

