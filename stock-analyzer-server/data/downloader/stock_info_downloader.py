"""
Download interested tickers name info
"""

import akshare as ak
from tqdm import tqdm

from data.tickers import tickers
from data.utils import Connect, setup_stock_info_table

df = ak.stock_hk_spot()


def _download_stock_info(ticker):
    name = list(df[df.symbol == '0{}'.format(ticker[:4])]['name'])[0]
    return [ticker, name]


def _save_stock_info(data):
    setup_stock_info_table()
    with Connect() as conn:
        conn.executemany('INSERT INTO stock_info VALUES (?,?)', data)
        conn.commit()


def download():
    print('Download stock info ...')
    data = [_download_stock_info(ticker) for ticker in tqdm(tickers)]
    _save_stock_info(data)


if __name__ == '__main__':
    download()
