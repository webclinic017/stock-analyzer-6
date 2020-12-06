import os
from functools import lru_cache
from pathlib import Path

import akshare as ak
import yaml

data_dir = Path(__file__).parent
root_dir = Path(__file__).parent.parent


@lru_cache()
def get_stock_hk_spot():
    return ak.stock_hk_spot()


def _tickers():
    """ Interest tickers consists of 2 parts
    - 1. Volume larger than 60 mm
    - 2. Hard coded interested tickers from config """
    df = get_stock_hk_spot()
    df.amount = [float(i) for i in df.amount]
    df = df[df.amount >= 60000000.0]
    interested_tickers = ['{}.HK'.format(symbol[1:]) for symbol in list(df['symbol'])]

    with open(os.path.join(root_dir, 'config.yml')) as file:
        for ticker in yaml.load(file, Loader=yaml.FullLoader)['tickers']:
            if ticker not in interested_tickers:
                interested_tickers.append(ticker)

    return interested_tickers


tickers = _tickers()
