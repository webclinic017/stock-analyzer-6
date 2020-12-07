"""
Download interested tickers' 10 years OHLC data
"""

import datetime

from tqdm import tqdm
from yahoo_historical import Fetcher

from data.tickers import tickers
from data.db import Connect, setup_ohlc_table


def _download_ticker_data(ticker):
    """ Download data for ticker """
    today = datetime.date.today()
    start = [today.year-10, today.month, today.day]
    end = [today.year, today.month, today.day+1]
    data = Fetcher(ticker, start, end)
    data = data.get_historical()
    cols = ['Ticker'] + list(data.columns)
    data['Ticker'] = [ticker for _ in range(len(data))]
    data = data[cols]
    data.dropna(inplace=True)
    return data


def _save_ticker_data(data):
    with Connect() as conn:
        conn.executemany('INSERT INTO ohlc VALUES (?,?,?,?,?,?,?,?)', data.values.tolist())
        conn.commit()


def download():
    print('Download stock ohlc data ...')
    setup_ohlc_table()
    for ticker in tqdm(tickers):
        data = _download_ticker_data(ticker)
        _save_ticker_data(data)


if __name__ == '__main__':
    # download()
    print(_download_ticker_data('^HSI'))
