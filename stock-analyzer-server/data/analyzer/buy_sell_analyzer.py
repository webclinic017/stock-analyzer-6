import pandas as pd

from data.analyzer.utils import calc_boll, calc_macd, calc_kdj
from data.analyzer.utils import (
    get_prices, get_price_change, get_last_price, get_ticker_name, get_ticker_volume
)
from data.tickers import tickers
from data.db import setup_buy_sell_table, Connect
from tqdm import tqdm


# Buy sell based on boll values
def _boll_analysis(ticker):
    """ if res > 1, should sell, if val < 1, should buy, others remain """
    prices = get_prices(ticker, 100)
    boll, upper, lower = calc_boll(prices)
    close = prices[-1][3]
    res = (close - boll[-1]) / (upper[-1] - lower[-1]) * 2
    if pd.isnull(res):
        res = 0
    return res


# Buy sell based on macd
def _macd_analysis(ticker):
    prices = get_prices(ticker, 100)
    dif, dea, macd = calc_macd(prices)
    try:
        if macd[-2] < 0 and macd[-2] == min(macd[-3], macd[-2], macd[-1]):
            return 'TU'  # Turn up
        elif macd[-2] > 0 and macd[-2] == max(macd[-3], macd[-2], macd[-1]):
            return 'TD'  # Turn down
        elif 0 > dif[-1] >= dea[-1] and dif[-2] <= dea[-2]:
            return 'GC'  # Gold cross
        elif 0 < dif[-1] <= dea[-1] and dif[-2] >= dea[-2]:
            return 'DC'  # Dead cross
    except:
        return ''
    return ''


# Buy sell based on KDJ
def _kdj_analysis(ticker):
    prices = get_prices(ticker, 100)
    k, d, j = calc_kdj(prices)
    try:
        a = k[-1] - d[-1]
        b = k[-2] - d[-2]
        if a * b <= 0:
            if 70 < k[-1] <= d[-1]:
                return 'HDC'  # High death cross
            elif d[-1] <= k[-1] < 30:
                return 'LGC'  # Low gold cross
    except:
        return ''
    return ''


def _analyse_buy_sell(ticker):
    try:
        name = get_ticker_name(ticker)
        price = get_last_price(ticker)
        _, increase_rate = get_price_change(ticker)
        volume = get_ticker_volume(ticker)
        boll_1d = _boll_analysis(ticker)
        macd_1d = _macd_analysis(ticker)
        kdj_1d = _kdj_analysis(ticker)
        return ticker, name, price, increase_rate, boll_1d, macd_1d, kdj_1d, volume
    except:
        print('Skip {}'.format(get_ticker_name(ticker)))
        return []


def _analyse_all_tickers():
    all_res = []
    for ticker in tqdm(tickers):
        res = _analyse_buy_sell(ticker)
        if res:
            all_res.append(res)
    return all_res


def _save_ticker_results(data):
    setup_buy_sell_table()
    with Connect() as conn:
        conn.executemany('INSERT INTO buy_sell VALUES (?,?,?,?,?,?,?, ?)', data)
        conn.commit()


def analyse():
    print('Analyze buy/sell indicators ...')
    data = _analyse_all_tickers()
    _save_ticker_results(data)


if __name__ == '__main__':
    analyse()
