import sqlite3

DB_NAME = "ticks.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            size REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_tick(tick):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO ticks VALUES (?, ?, ?, ?)",
        (
            tick["timestamp"],
            tick["symbol"],
            tick["price"],
            tick["size"],
        )
    )

    conn.commit()
    conn.close()
