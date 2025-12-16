# Quantitative Analytics Dashboard

## Overview

This project is a real-time analytical prototype designed to demonstrate end-to-end quantitative
development skills — from live market data ingestion to statistical analytics and interactive
visualization.

The system ingests real-time Binance Futures tick data, resamples it into time-based bars,
computes pair-trading analytics, and presents insights through an interactive dashboard.

---

## Architecture

The system follows a modular, loosely-coupled design:

- WebSocket Ingestion Layer
- Persistent Storage (SQLite)
- Resampling Engine
- Analytics Engine
- Interactive Frontend
- Alerting & Export Layer

Each component can be extended or replaced independently.

---

## Data Ingestion

- Source: Binance Futures WebSocket (`@trade` stream)
- Fields: timestamp, symbol, price, quantity
- Real-time async ingestion using Python `asyncio` + `websockets`

---

## Storage Strategy

- SQLite used as lightweight persistent storage
- Acts as source-of-truth for resampling & analytics
- Easy to replace with PostgreSQL / Redis for scale

---

## Resampling Logic

- Tick data resampled into OHLCV bars
- Supported intervals: 1s, 1min, 5min
- Resampling computed on demand to avoid unnecessary recomputation

---

## Analytics Implemented

- Hedge Ratio (OLS Regression)
- Spread computation
- Rolling Z-score
- Rolling Correlation
- ADF Stationarity Test (guarded for sufficient data)

All analytics handle live-data edge cases gracefully.

---

## Live Update Strategy

- WebSocket ingestion runs continuously
- UI refreshes near-real-time
- Analytics enabled only when sufficient data is available

---

## Alerts

- Rule-based alerting using Z-score thresholds
- Visual alerts triggered when |z-score| > 2

---

## Extensibility

The system is designed to:

- Plug in alternative data sources (CSV, REST, other exchanges)
- Add new analytics modules without touching ingestion
- Scale storage and execution independently

---

## How to Run

```bash
pip install -r requirements.txt
python ws_ingest.py
streamlit run app.py

## ChatGPT Usage Disclosure
ChatGPT was used for:
- Boilerplate code generation
- Debugging assistance
- Structuring modular architecture

All design decisions, analytics selection, and system integration
were independently reasoned and implemented.
```
