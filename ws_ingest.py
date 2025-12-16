import asyncio
import json
import websockets
import signal
from datetime import datetime
from collections import deque

from storage import init_db, insert_tick


TICK_BUFFER = deque(maxlen=10000)
STOP = False   # manual stop flag


def normalize_trade(msg):
    ts = msg.get("T") or msg.get("E")
    return {
        "symbol": msg["s"],
        "timestamp": datetime.fromtimestamp(ts / 1000).isoformat(),
        "price": float(msg["p"]),
        "size": float(msg["q"]),
    }


def handle_stop(signum, frame):
    global STOP
    print("\nStopping gracefully...")
    STOP = True


async def listen_symbol(symbol):
    url = f"wss://fstream.binance.com/ws/{symbol.lower()}@trade"

    try:
        async with websockets.connect(url) as ws:
            print(f"Connected to {symbol}")

            while not STOP:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=1)
                except asyncio.TimeoutError:
                    continue

                data = json.loads(message)
                if data.get("e") == "trade":
                    tick = normalize_trade(data)
                    TICK_BUFFER.append(tick)
                    insert_tick(tick)
                    print(tick)

    except Exception as e:
        print(f"WebSocket closed for {symbol}: {e}")


async def main():
    init_db()
    symbols = ["btcusdt", "ethusdt"]
    tasks = [asyncio.create_task(listen_symbol(sym)) for sym in symbols]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_stop)  # CTRL+C handler
    asyncio.run(main())
