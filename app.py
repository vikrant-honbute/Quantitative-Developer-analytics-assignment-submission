import streamlit as st
import plotly.graph_objects as go

from resample import load_ticks, resample_ticks
from analytics.hedge import compute_hedge_ratio, compute_spread, compute_zscore
from analytics.correlation import rolling_correlation
from analytics.stationarity import adf_test


st.set_page_config(page_title="Quant Analytics Dashboard", layout="wide")
st.title("📊 Quantitative Analytics Dashboard")


# Sidebar
st.sidebar.header("Controls")

symbol_a = st.sidebar.selectbox("Symbol A", ["BTCUSDT", "ETHUSDT"])
symbol_b = st.sidebar.selectbox("Symbol B", ["ETHUSDT", "BTCUSDT"])

timeframe_label = st.sidebar.selectbox(
    "Timeframe",
    ["1 Second", "1 Minute", "5 Minutes"]
)

timeframe_map = {
    "1 Second": "1s",
    "1 Minute": "1min",
    "5 Minutes": "5min"
}

timeframe = timeframe_map[timeframe_label]


window = st.sidebar.slider("Rolling Window", 10, 60, 30)

run_adf = st.sidebar.button("Run ADF Test")


# Load & resample data

df_a = load_ticks(symbol_a)
df_b = load_ticks(symbol_b)

if df_a.empty or df_b.empty:
    st.warning("Waiting for tick data...")
    st.stop()

bars_a = resample_ticks(df_a, timeframe)
bars_b = resample_ticks(df_b, timeframe)

data = bars_a.join(bars_b, lsuffix="_a", rsuffix="_b").dropna()

if len(data) < window:
    st.warning("Not enough data for analytics yet.")
    st.stop()

price_a = data["close_a"]
price_b = data["close_b"]


# Analytics

hedge_ratio = compute_hedge_ratio(price_a, price_b)
spread = compute_spread(price_a, price_b, hedge_ratio)
zscore = compute_zscore(spread, window)
correlation = rolling_correlation(price_a, price_b, window)


# Data Export

st.sidebar.subheader("Export")

if st.sidebar.button("Download Analytics CSV"):
    export_df = data.copy()
    export_df["spread"] = spread
    export_df["zscore"] = zscore
    export_df["correlation"] = correlation

    csv = export_df.dropna().to_csv().encode("utf-8")

    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="analytics_output.csv",
        mime="text/csv"
    )


# Layout

col1, col2 = st.columns(2)

# Price chart
with col1:
    st.subheader("Prices")

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=price_a.index, y=price_a, name=symbol_a))
    fig_price.add_trace(go.Scatter(x=price_b.index, y=price_b, name=symbol_b))

    st.plotly_chart(fig_price, use_container_width=True)

# Spread & Z-score
with col2:
    st.subheader("Spread & Z-Score")

    fig_spread = go.Figure()
    fig_spread.add_trace(go.Scatter(x=spread.index, y=spread, name="Spread"))
    fig_spread.add_trace(go.Scatter(x=zscore.index, y=zscore, name="Z-score", yaxis="y2"))

    fig_spread.update_layout(
        yaxis=dict(title="Spread"),
        yaxis2=dict(title="Z-score", overlaying="y", side="right"),
    )

    st.plotly_chart(fig_spread, use_container_width=True)

# Correlation
st.subheader("Rolling Correlation")

fig_corr = go.Figure()
fig_corr.add_trace(go.Scatter(x=correlation.index, y=correlation, name="Correlation"))
st.plotly_chart(fig_corr, use_container_width=True)


# Stats & Alerts

st.subheader("Statistics")

col3, col4, col5 = st.columns(3)

col3.metric("Hedge Ratio", round(hedge_ratio, 4))

z_clean = zscore.dropna()
if len(z_clean) > 0:
    col4.metric("Latest Z-score", round(z_clean.iloc[-1], 3))
else:
    col4.metric("Latest Z-score", "N/A")
