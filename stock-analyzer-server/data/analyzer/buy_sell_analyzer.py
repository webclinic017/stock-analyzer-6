from data.analyzer.utils import get_prices, calc_boll, calc_macd
from data.tickers import tickers

import pandas as pd


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


if __name__ == '__main__':
    for ticker in tickers:
        print(ticker, _boll_analysis(ticker), _macd_analysis(ticker))
