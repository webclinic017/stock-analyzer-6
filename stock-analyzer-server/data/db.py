import os
import sqlite3
from pathlib import Path

data_dir = Path(__file__).parent
root_dir = Path(__file__).parent.parent


class Connect(object):
    DB_PATH = os.path.join(data_dir, 'store.db')

    def __enter__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def setup_ohlc_table():
    """ Clear data of ohlc table """
    drop_sql = """DROP TABLE IF EXISTS ohlc;"""
    create_sql = """CREATE TABLE IF NOT EXISTS ohlc (
        ticker text,
        date text,
        open real,
        high real,
        low real,
        close real,
        adjclose real,
        volume real
    );"""
    with Connect() as conn:
        conn.execute(drop_sql)
        conn.execute(create_sql)


def setup_hsi_table():
    """ Clear data of hsi table """
    drop_sql = """DROP TABLE IF EXISTS hsi;"""
    create_sql = """CREATE TABLE IF NOT EXISTS hsi (
        date text,
        open real,
        high real,
        low real,
        close real,
        adjclose real,
        volume real
    );"""
    with Connect() as conn:
        conn.execute(drop_sql)
        conn.execute(create_sql)


def setup_stock_info_table():
    """ Clear data of stock info table """
    drop_sql = """DROP TABLE IF EXISTS stock_info;"""
    create_sql = """CREATE TABLE IF NOT EXISTS stock_info (
        ticker text, 
        name text
    );"""
    with Connect() as conn:
        conn.execute(drop_sql)
        conn.execute(create_sql)


def setup_strong_stock_table():
    """ Clear data of strong stocks table """
    drop_sql = """DROP TABLE IF EXISTS strong_stocks;"""
    create_sql = """CREATE TABLE IF NOT EXISTS strong_stocks (
        ticker text, 
        name text,
        price real,
        increase real,
        increase_rate real,
        rel_1d real, 
        rel_5d real, 
        rel_20d real, 
        cs real, 
        sm real, 
        ml real,
        volume real
    );"""
    with Connect() as conn:
        conn.execute(drop_sql)
        conn.execute(create_sql)


def setup_buy_sell_table():
    """ Clear data of strong stocks table """
    drop_sql = """DROP TABLE IF EXISTS buy_sell;"""
    create_sql = """CREATE TABLE IF NOT EXISTS buy_sell (
        ticker text, 
        name text,
        price real,
        increase_rate real,
        boll_rel_1d real, 
        macd_1d text,
        kdj_1d text,
        volume real
    );"""
    with Connect() as conn:
        conn.execute(drop_sql)
        conn.execute(create_sql)
