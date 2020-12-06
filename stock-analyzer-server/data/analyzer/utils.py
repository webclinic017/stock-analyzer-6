import pandas as pd


def calc_ema(prices, span=5, precision=2):
    df = pd.DataFrame([[p] for p in prices], columns=['price'])
    df = df.ewm(span=span, adjust=False).mean()
    return [round(v, precision) for v in list(df['price'])]
