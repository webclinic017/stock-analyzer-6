import pandas as pd

from data.analyzer.utils import calc_boll, calc_macd
from data.analyzer.utils import (
    get_prices, get_price_change, get_last_price, get_ticker_name, get_ticker_volume
)
from data.tickers import tickers
from data.utils import setup_buy_sell_table, Connect
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
        elif dif[-1] >= dea[-1] and dif[-2] <= dea[-2]:
            return 'GC'  # Gold cross
        elif dif[-1] <= dea[-1] and dif[-2] >= dea[-2]:
            return 'DC'  # Dead cross
    except:
        return ''
    return ''


def _analyse_buy_sell(ticker):
    try:
        name = get_ticker_name(ticker)
        price = get_last_price(ticker)
        _, increase_rate = get_price_change(ticker)
        volume = get_ticker_volume(ticker)
        boll = _boll_analysis(ticker)
        return [ticker, name, price, increase_rate, boll, volume]
    except:
        print('Skip {}'.format(get_ticker_name(ticker)))


def _save_ticker_results(data):
    setup_buy_sell_table()
    with Connect() as conn:
        conn.executemany('INSERT INTO buy_sell VALUES (?,?,?,?,?,?,?,?)', data)
        conn.commit()


def analyse():
    print('Analyze buy/sell indicators ...')
    data = [_analyse_buy_sell(ticker) for ticker in tqdm(tickers)]
    _save_ticker_results(data)


if __name__ == '__main__':
    print(_analyse_buy_sell('0700.HK'))
