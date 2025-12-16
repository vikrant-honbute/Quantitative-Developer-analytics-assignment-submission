import sqlite3
import pandas as pd


DB_NAME = "ticks.db"


def load_ticks(symbol):
    """
    Load ticks for a symbol from SQLite
    """
    conn = sqlite3.connect(DB_NAME)

    query = """
        SELECT timestamp, price, size
        FROM ticks
        WHERE symbol = ?
        ORDER BY timestamp
    """

    df = pd.read_sql(query, conn, params=(symbol,))
    conn.close()

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")

    df.set_index("timestamp", inplace=True)

    return df


def resample_ticks(df, timeframe):
    """
    Resample ticks into OHLCV bars

    timeframe: '1S', '1T', '5T'
    """
    ohlc = df["price"].resample(timeframe).ohlc()
    volume = df["size"].resample(timeframe).sum()

    bars = ohlc.copy()
    bars["volume"] = volume

    bars.dropna(inplace=True)
    return bars
