import numpy as np
import pandas as pd
import statsmodels.api as sm


def compute_hedge_ratio(series_a, series_b):
    """
    OLS regression: A = alpha + beta * B
    beta = hedge ratio
    """
    series_b = sm.add_constant(series_b)
    model = sm.OLS(series_a, series_b).fit()
    hedge_ratio = model.params.iloc[1]

    return hedge_ratio


def compute_spread(series_a, series_b, hedge_ratio):
    """
    Spread = A - beta * B
    """
    return series_a - hedge_ratio * series_b


def compute_zscore(spread, window=30):
    """
    Rolling z-score
    """
    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std()
    zscore = (spread - mean) / std
    return zscore
