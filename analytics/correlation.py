def rolling_correlation(series_a, series_b, window=30):
    return series_a.rolling(window).corr(series_b)
