from resample import load_ticks, resample_ticks
from analytics.hedge import compute_hedge_ratio, compute_spread, compute_zscore
from analytics.correlation import rolling_correlation
from analytics.stationarity import adf_test

# load data
df_a = load_ticks("BTCUSDT")
df_b = load_ticks("ETHUSDT")

bars_a = resample_ticks(df_a, "1min")
bars_b = resample_ticks(df_b, "1min")


# align timestamps
data = bars_a.join(bars_b, lsuffix="_a", rsuffix="_b").dropna()

price_a = data["close_a"]
price_b = data["close_b"]

hedge = compute_hedge_ratio(price_a, price_b)
spread = compute_spread(price_a, price_b, hedge)
zscore = compute_zscore(spread)

corr = rolling_correlation(price_a, price_b)
adf = adf_test(spread)

print("Hedge Ratio:", hedge)
zscore_clean = zscore.dropna()

if len(zscore_clean) > 0:
    print("Latest Z-score:", zscore_clean.iloc[-1])
else:
    print("Latest Z-score: Not enough data yet")

print("ADF Result:", adf)
