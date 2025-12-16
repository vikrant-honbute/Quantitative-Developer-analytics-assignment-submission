from statsmodels.tsa.stattools import adfuller


def adf_test(series, min_samples=30):
    """
    Augmented Dickey-Fuller test with safety check
    """
    series = series.dropna()

    if len(series) < min_samples:
        return {
            "adf_statistic": None,
            "p_value": None,
            "is_stationary": None,
            "message": f"Not enough data for ADF (need {min_samples}, got {len(series)})"
        }

    result = adfuller(series)
    return {
        "adf_statistic": result[0],
        "p_value": result[1],
        "is_stationary": result[1] < 0.05,
        "message": "ADF test successful"
    }
