from data.downloader.stock_info_downloader import download as download_stock_info
from data.downloader.ohlc_downloader import download as download_stock_ohlc_data
from data.downloader.hsi_downloader import download as download_hsi_data

from data.analyzer.strong_stocks_analyzer import analyze as analyze_strong_stocks


def _download_all_raw_data():
    download_stock_info()
    download_stock_ohlc_data()
    download_hsi_data()


def _analyze_all_data():
    analyze_strong_stocks()


def prepare_all_data():
    _download_all_raw_data()
    _analyze_all_data()


if __name__ == '__main__':
    prepare_all_data()
