"""
Download 10 years Heng Seng Index (HSI) OHLC data
"""

import datetime
import time
from io import StringIO

import pandas as pd
import requests

from data.utils import Connect, setup_hsi_table

url = 'https://query1.finance.yahoo.com/v7/finance/download/%5EHSI' \
      '?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'


def _download_hsi_data():
    today = datetime.date.today()
    start = [today.year - 10, today.month, today.day]
    end = [today.year, today.month, today.day]
    period1 = int(time.mktime(datetime.date(*start).timetuple()))
    period2 = int(time.mktime(datetime.date(*end).timetuple()))
    for _ in range(5):
        try:
            res = requests.get(url.format(period1=period1, period2=period2))
            data = StringIO(res.content.decode('utf-8'))
            data = pd.read_csv(data, sep=',')
            return data
        except:
            time.sleep(10)


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
