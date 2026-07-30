"""Technical signals. Each scorer returns 0-100 where 50 = neutral,
>50 = bullish evidence, <50 = bearish evidence."""
import numpy as np
import pandas as pd

def sma(s, n): return s.rolling(n).mean()

def rsi(close, n=14):
    delta = close.diff()
    up = delta.clip(lower=0).ewm(alpha=1/n, min_periods=n).mean()
    dn = (-delta.clip(upper=0)).ewm(alpha=1/n, min_periods=n).mean()
    rs = up / dn.replace(0, np.nan)
    return 100 - 100 / (1 + rs)

def macd(close, fast=12, slow=26, sig=9):
    line = close.ewm(span=fast).mean() - close.ewm(span=slow).mean()
    signal = line.ewm(span=sig).mean()
    return line, signal, line - signal

def clamp(x, lo=0, hi=100): return float(max(lo, min(hi, x)))

def score_trend(df):
    c = df["Close"]
    s20, s50 = sma(c, 20).iloc[-1], sma(c, 50).iloc[-1]
    px = c.iloc[-1]
    ret1m = (px / c.iloc[-21] - 1) * 100 if len(c) > 21 else 0
    score = 50 + (12 if s20 > s50 else -12) + (8 if px > s20 else -8) + clamp(ret1m * 2, -15, 15)
    note = (f"SMA20 {'above' if s20 > s50 else 'below'} SMA50, price {'above' if px > s20 else 'below'} SMA20, "
            f"1-month return {ret1m:+.1f}%")
    return clamp(score), note

def score_rsi(df):
    r = rsi(df["Close"]).iloc[-1]
    if pd.isna(r): return 50.0, "RSI unavailable"
    if r >= 70: score, tag = 35, "overbought — chase risk"
    elif r >= 55: score, tag = 68, "bullish momentum zone"
    elif r >= 45: score, tag = 50, "neutral"
    elif r >= 30: score, tag = 38, "bearish momentum zone"
    else: score, tag = 60, "oversold — bounce candidate"
    return float(score), f"RSI(14) = {r:.0f} ({tag})"

def score_macd(df):
    line, signal, hist = macd(df["Close"])
    l, s, h = line.iloc[-1], signal.iloc[-1], hist.iloc[-1]
    rising = hist.iloc[-1] > hist.iloc[-3] if len(hist) > 3 else False
    score = 50 + (12 if l > s else -12) + (8 if rising else -8)
    note = f"MACD {'above' if l > s else 'below'} signal, histogram {'rising' if rising else 'falling'}"
    return clamp(score), note

def score_volume(df):
    v = df["Volume"]
    avg = v.rolling(20).mean().iloc[-1]
    ratio = float(v.iloc[-1] / avg) if avg else 1.0
    # Volume confirms the day's direction
    up_day = df["Close"].iloc[-1] >= df["Open"].iloc[-1]
    if ratio >= 1.5:
        score = 50 + (20 if up_day else -20) * min(ratio / 1.5, 2)
        note = f"volume spike {ratio:.1f}x 20-day avg on {'an up' if up_day else 'a down'} day"
    else:
        score, note = 50, f"volume {ratio:.1f}x 20-day avg (no spike)"
    return clamp(score), note, ratio

def score_rel_strength(df, spy_df):
    c, s = df["Close"], spy_df["Close"]
    if len(c) < 22 or len(s) < 22: return 50.0, "insufficient history"
    rs = ((c.iloc[-1]/c.iloc[-21]) - (s.iloc[-1]/s.iloc[-21])) * 100
    return clamp(50 + rs * 3), f"1-month return vs SPY: {rs:+.1f}%"

def hv_percentile(df, window=20, lookback=252):
    lr = np.log(df["Close"] / df["Close"].shift(1))
    hv = lr.rolling(window).std() * np.sqrt(252) * 100
    hv = hv.dropna().tail(lookback)
    if len(hv) < 40: return None, None
    cur = hv.iloc[-1]
    pctl = float((hv < cur).mean() * 100)
    return float(cur), pctl

def score_volatility(df):
    cur, pctl = hv_percentile(df)
    if cur is None: return 50.0, "volatility history unavailable", None
    # Sweet spot: enough movement to pay off an option, not blow-off extremes
    if pctl >= 85: score, tag = 38, "extreme — options likely overpriced"
    elif pctl >= 55: score, tag = 60, "elevated — good movement potential"
    elif pctl >= 30: score, tag = 52, "normal"
    else: score, tag = 42, "sleepy — option may decay before a move"
    return float(score), f"20-day HV {cur:.0f}%, {pctl:.0f}th percentile of past year ({tag})", pctl

POS_WORDS = ("beat","beats","surge","soar","record","upgrade","upgraded","rally","jump","strong",
             "growth","wins","approval","approved","raises","raised","bullish","breakout","partnership")
NEG_WORDS = ("miss","misses","plunge","fall","falls","drop","downgrade","downgraded","lawsuit","probe",
             "recall","cuts","cut","layoff","layoffs","warning","warns","bearish","fraud","halt","bankruptcy")

def score_sentiment(news_items):
    """news_items: list of headline strings (from yfinance Ticker.news — free, keyless)."""
    if not news_items: return 50.0, "no recent headlines found — neutral"
    pos = neg = 0
    for h in news_items[:12]:
        t = h.lower()
        pos += sum(w in t for w in POS_WORDS)
        neg += sum(w in t for w in NEG_WORDS)
    if pos == neg: return 50.0, f"{len(news_items)} headlines, mixed/neutral tone"
    score = clamp(50 + (pos - neg) * 8)
    return score, f"{len(news_items)} headlines: {pos} positive vs {neg} negative keyword hits"


def score_congress(ticker, activity):
    """Elite flows: recent lawmaker/insider buys vs sells. >50 = net buying."""
    a = (activity or {}).get(ticker)
    if not a or (a["buys"] == 0 and a["sells"] == 0):
        return 50.0, "no recent lawmaker trades on file"
    net = a["buys"] - a["sells"]
    who = ", ".join(a["names"][:2]) if a["names"] else ""
    tag = f" (incl. {who})" if who else ""
    return clamp(50 + net * 7), f"{a['buys']} buys / {a['sells']} sells by lawmakers in last 90d{tag}"

def score_social(ticker, buzz):
    """Retail social buzz. Mild bull/bear tilt; extreme hype is treated cautiously."""
    b = (buzz or {}).get(ticker)
    if not b or b["mentions"] == 0:
        return 50.0, "no notable social buzz"
    tone = b["bull"] - b["bear"]
    score = 50 + tone * 4 + min(b["mentions"], 8)
    if b["mentions"] >= 12:  # hype extreme -> fade slightly
        score -= 6
    trend = " (StockTwits trending)" if b["trending"] else ""
    return clamp(score), f"{b['mentions']} social mentions, tone {tone:+d}{trend}"
