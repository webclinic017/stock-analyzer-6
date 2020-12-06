"""
Analyze strong stock indicators value
"""

from data.analyzer.utils import calc_ema
from data.utils import Connect, setup_strong_stock_table
from data.tickers import tickers

from tqdm import tqdm
import akshare as ak


def _hsi_baseline():
    sql = """
        SELECT adjclose
        FROM hsi
        ORDER BY DATE Desc
        LIMIT 21
    """
    prices = []
    with Connect() as conn:
        cur = conn.execute(sql)
        for row in cur.fetchall():
            prices.append(row[0])
    increase_rate_1d = (prices[0] - prices[1]) / prices[1] * 100
    increase_rate_5d = (prices[0] - prices[5]) / prices[5] * 100
    increase_rate_20d = (prices[0] - prices[20]) / prices[20] * 100
    return increase_rate_1d, increase_rate_5d, increase_rate_20d


def _get_ticker_prices(ticker, look_back_days, date_descending=True):
    sql = """
        SELECT adjclose
        FROM ohlc
        WHERE ticker = '{}'
        ORDER BY DATE Desc
        LIMIT {}
    """.format(ticker, look_back_days)
    prices = []
    with Connect() as conn:
        cur = conn.execute(sql)
        for row in cur.fetchall():
            prices.append(row[0])
    if not date_descending:
        prices = prices[::-1]
    return prices


def _ticker_increase_rate(ticker):
    prices = _get_ticker_prices(ticker, 21)
    increase_rate_1d = (prices[0] - prices[1]) / prices[1] * 100
    increase_rate_5d = (prices[0] - prices[5]) / prices[5] * 100
    increase_rate_20d = (prices[0] - prices[20]) / prices[20] * 100
    return increase_rate_1d, increase_rate_5d, increase_rate_20d


def _c_divide_s(ticker):
    """ (Close - EMA20) / EMA20 * 100 """
    prices = _get_ticker_prices(ticker, 21, date_descending=False)
    close = prices[-1]
    ema20 = calc_ema(prices, 20)[-1]
    return (close - ema20) / ema20 * 100


def _s_divide_m(ticker):
    """ (EMA20 - EMA60) / EMA60 * 100 """
    prices = _get_ticker_prices(ticker, 61, date_descending=False)
    ema20 = calc_ema(prices, 20)[-1]
    ema60 = calc_ema(prices, 60)[-1]
    return (ema20 - ema60) / ema60 * 100


def _m_divide_l(ticker):
    """ (EMA60 - EMA120) / EMA120 * 100 """
    prices = _get_ticker_prices(ticker, 121, date_descending=False)
    ema60 = calc_ema(prices, 60)[-1]
    ema120 = calc_ema(prices, 120)[-1]
    return (ema60 - ema120) / ema120 * 100


def _price_change(ticker):
    prices = _get_ticker_prices(ticker, 2)
    return prices[0] - prices[1], (prices[0] / prices[1] - 1) * 100


def _ticker_name(ticker):
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


df = ak.stock_hk_spot()


def _ticker_volume(ticker):
    return float(list(df[df.symbol == '0{}'.format(ticker[:4])]['amount'])[0])


def _analyze_ticker(ticker):
    hsi_increase_1d, hsi_increase_5d, hsi_increase_20d = _hsi_baseline()
    ticker_increase_1d, ticker_increase_5d, ticker_increase_20d = _ticker_increase_rate(ticker)
    name = _ticker_name(ticker)
    price = _get_ticker_prices(ticker, 1)[0]
    increase, increase_rate = _price_change(ticker)
    rel_1d = ticker_increase_1d - hsi_increase_1d
    rel_5d = ticker_increase_5d - hsi_increase_5d
    rel_20d = ticker_increase_20d - hsi_increase_20d
    cs = _c_divide_s(ticker)
    sm = _s_divide_m(ticker)
    ml = _m_divide_l(ticker)
    volume = _ticker_volume(ticker)
    return [ticker, name, price, increase, increase_rate, rel_1d, rel_5d, rel_20d, cs, sm, ml, volume]


def _analyze_all_tickers():
    res = []
    for ticker in tqdm(tickers):
        try:
            res.append(_analyze_ticker(ticker))
        except:
            print('Skip {}'.format(_ticker_name(ticker)))
    return res


def _save_ticker_results(data):
    setup_strong_stock_table()
    with Connect() as conn:
        conn.executemany('INSERT INTO strong_stocks VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', data)
        conn.commit()


def analyze():
    print('Analyze strong stocks ...')
    data = _analyze_all_tickers()
    _save_ticker_results(data)


if __name__ == '__main__':
    analyze()
