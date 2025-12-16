from resample import load_ticks, resample_ticks

df = load_ticks("BTCUSDT")

bars_1s = resample_ticks(df, "1S")
bars_1m = resample_ticks(df, "1T")
bars_5m = resample_ticks(df, "5T")

print("1s bars:")
print(bars_1s.tail())

print("\n1m bars:")
print(bars_1m.tail())

print("\n5m bars:")
print(bars_5m.tail())
