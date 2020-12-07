"""
Download 10 years Heng Seng Index (HSI) OHLC data
"""

import datetime

from yahoo_historical import Fetcher

from data.db import Connect, setup_hsi_table


def _download_hsi_data():
    """ Download data for ticker """
    today = datetime.date.today()
    start = [today.year - 10, today.month, today.day]
    end = [today.year, today.month, today.day + 1]
    data = Fetcher('^HSI', start, end)
    data = data.get_historical()
    return data


def _save_hsi_data(data):
    setup_hsi_table()
    with Connect() as conn:
        conn.executemany('INSERT INTO hsi VALUES (?,?,?,?,?,?,?)', data.values.tolist())
        conn.commit()


def download():
    print('Download hsi data ...')
    data = _download_hsi_data()
    _save_hsi_data(data)


if __name__ == '__main__':
    download()
