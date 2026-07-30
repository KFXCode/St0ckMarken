"""Data fetching — Yahoo Finance via yfinance. Free, keyless."""
import time
import pandas as pd
import yfinance as yf

def fetch_history(tickers, period="1y"):
    """Batch-download daily OHLCV. Returns {ticker: DataFrame}."""
    out = {}
    data = yf.download(tickers, period=period, interval="1d", group_by="ticker",
                       auto_adjust=True, progress=False, threads=True)
    for t in tickers:
        try:
            df = data[t].dropna() if isinstance(data.columns, pd.MultiIndex) else data.dropna()
            if len(df) >= 60:
                out[t] = df
        except Exception:
            continue
    return out

def fetch_news(ticker):
    """Recent headline strings for a ticker (best-effort)."""
    try:
        items = yf.Ticker(ticker).news or []
        heads = []
        for it in items:
            c = it.get("content", it)
            h = c.get("title") or ""
            if h: heads.append(h)
        return heads
    except Exception:
        return []

def fetch_chain(ticker, dte_min, dte_max):
    """Return (expiry_str, calls_df, puts_df, spot) for the first expiry in the DTE window."""
    try:
        tk = yf.Ticker(ticker)
        spot = tk.fast_info.get("lastPrice") or tk.fast_info.get("last_price")
        expiries = tk.options or []
        today = pd.Timestamp.utcnow().tz_localize(None).normalize()
        for e in expiries:
            dte = (pd.Timestamp(e) - today).days
            if dte_min <= dte <= dte_max:
                ch = tk.option_chain(e)
                return e, ch.calls, ch.puts, float(spot)
        return None, None, None, float(spot) if spot else None
    except Exception:
        return None, None, None, None

def fetch_earnings_date(ticker):
    """Next earnings date (Timestamp) or None."""
    try:
        cal = yf.Ticker(ticker).calendar
        dates = cal.get("Earnings Date") if isinstance(cal, dict) else None
        if dates:
            return pd.Timestamp(dates[0])
    except Exception:
        pass
    return None

def polite_pause():
    time.sleep(0.4)  # be gentle with Yahoo's free endpoints
