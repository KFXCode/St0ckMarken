"""Candlestick pattern recognition — from 'The Candlestick Trading Bible'.
Detects the book's core reversal/continuation patterns on daily OHLC bars and
explains each in plain, 5th-grade language. Feeds a 'candles' scoring factor
and a per-trade 'patterns spotted' box in the report.

Works on any OHLC series, so the same engine reads US stocks AND forex candles."""
import pandas as pd

def _body(o, c): return abs(c - o)
def _rng(h, l): return (h - l) or 1e-9
def _upper(o, h, c): return h - max(o, c)
def _lower(o, l, c): return min(o, c) - l

def detect(df):
    """Return list of {name, dir ('bull'|'bear'), plain} for patterns on the latest bars.
    dir = which way the pattern says price may go next."""
    if df is None or len(df) < 4:
        return []
    o = df["Open"].values; h = df["High"].values
    l = df["Low"].values;  c = df["Close"].values
    # short prevailing trend from the 5 bars before the signal bar
    prior = c[-6:-1]
    downtrend = prior[-1] < prior[0]
    uptrend = prior[-1] > prior[0]
    out = []
    i = -1  # signal bar = most recent completed daily candle
    body = _body(o[i], c[i]); rng = _rng(h[i], l[i])
    up = _upper(o[i], h[i], c[i]); lo = _lower(o[i], l[i], c[i])
    green = c[i] > o[i]; red = c[i] < o[i]

    # --- Hammer / Shooting Star (single-bar rejection) ---
    if lo >= 2 * body and up <= body and body > 0:
        if downtrend:
            out.append(("Hammer", "bull",
                "A candle with a long tail poking DOWN. It means sellers pushed the price down but buyers slapped it right back up — buyers are taking over."))
    if up >= 2 * body and lo <= body and body > 0:
        if uptrend:
            out.append(("Shooting Star", "bear",
                "A candle with a long tail poking UP. Buyers tried to push higher but sellers knocked it back down — sellers are taking over."))

    # --- Pin bar (either direction, long wick = rejection) ---
    if up >= 0.6 * rng and body <= 0.35 * rng:
        out.append(("Bearish Pin Bar", "bear",
            "A skinny candle with a tall top wick. The market poked up high, got rejected, and closed low — like a 'no thanks' to higher prices."))
    if lo >= 0.6 * rng and body <= 0.35 * rng:
        out.append(("Bullish Pin Bar", "bull",
            "A skinny candle with a long bottom wick. The market dipped, got rejected, and closed back up — like a 'no thanks' to lower prices."))

    # --- Doji family (open ≈ close) ---
    if body <= 0.1 * rng:
        if lo >= 2 * (up + body) and up <= body:
            out.append(("Dragonfly Doji", "bull",
                "Looks like a T. Price fell but came all the way back — buyers won the day. Often a bottom."))
        elif up >= 2 * (lo + body) and lo <= body:
            out.append(("Gravestone Doji", "bear",
                "Looks like an upside-down T. Price rose but fell all the way back — sellers won. Often a top."))
        else:
            out.append(("Doji", "bull" if downtrend else "bear",
                "Open and close are almost the same — a tug-of-war tie. The trend is losing steam and may flip."))

    # --- Engulfing (2-bar) ---
    if green and c[i-1] < o[i-1] and c[i] >= o[i-1] and o[i] <= c[i-1]:
        out.append(("Bullish Engulfing", "bull",
            "Today's green candle completely swallows yesterday's red one. Buyers overpowered sellers in a big way."))
    if red and c[i-1] > o[i-1] and o[i] >= c[i-1] and c[i] <= o[i-1]:
        out.append(("Bearish Engulfing", "bear",
            "Today's red candle completely swallows yesterday's green one. Sellers overpowered buyers in a big way."))

    # --- Harami (2-bar, small inside prior body) ---
    if _body(o[i-1], c[i-1]) > 0 and body < _body(o[i-1], c[i-1]) * 0.6 \
       and max(o[i], c[i]) <= max(o[i-1], c[i-1]) and min(o[i], c[i]) >= min(o[i-1], c[i-1]):
        if downtrend and c[i-1] < o[i-1]:
            out.append(("Bullish Harami", "bull",
                "A small candle tucked inside yesterday's big red one. The falling has paused — a turn up may be coming."))
        elif uptrend and c[i-1] > o[i-1]:
            out.append(("Bearish Harami", "bear",
                "A small candle tucked inside yesterday's big green one. The rally has paused — a turn down may be coming."))

    # --- Inside bar (today fully inside yesterday's high-low) ---
    if h[i] < h[i-1] and l[i] > l[i-1]:
        out.append(("Inside Bar", "bull" if uptrend else "bear",
            "Today stayed completely inside yesterday's range — the market is resting and squeezing. A breakout usually follows the trend."))

    # --- Tweezers (2-bar matching extremes) ---
    if abs(l[i] - l[i-1]) <= 0.0015 * c[i] and downtrend:
        out.append(("Tweezer Bottom", "bull",
            "Two candles with almost the same LOW — price hit a floor twice and bounced. Support is holding."))
    if abs(h[i] - h[i-1]) <= 0.0015 * c[i] and uptrend:
        out.append(("Tweezer Top", "bear",
            "Two candles with almost the same HIGH — price hit a ceiling twice and stalled. Resistance is holding."))

    # --- Morning / Evening Star (3-bar) ---
    if c[i-2] < o[i-2] and _body(o[i-1], c[i-1]) < _body(o[i-2], c[i-2]) * 0.6 and green and c[i] > (o[i-2] + c[i-2]) / 2:
        out.append(("Morning Star", "bull",
            "Three candles: a big red, a tiny pause, then a big green. Classic 'sun coming up' bottom — buyers take charge."))
    if c[i-2] > o[i-2] and _body(o[i-1], c[i-1]) < _body(o[i-2], c[i-2]) * 0.6 and red and c[i] < (o[i-2] + c[i-2]) / 2:
        out.append(("Evening Star", "bear",
            "Three candles: a big green, a tiny pause, then a big red. Classic 'sun going down' top — sellers take charge."))

    # de-dup by name, keep order
    seen, uniq = set(), []
    for p in out:
        if p[0] not in seen:
            seen.add(p[0]); uniq.append(p)
    return uniq

def score_candles(df, direction_hint=None):
    """0-100: >50 if bullish patterns dominate, <50 if bearish. Returns (score, note, patterns)."""
    pats = detect(df)
    if not pats:
        return 50.0, "no clear candlestick pattern on the latest bar", []
    bull = sum(1 for p in pats if p[1] == "bull")
    bear = sum(1 for p in pats if p[1] == "bear")
    score = 50 + (bull - bear) * 12
    score = max(0, min(100, score))
    names = ", ".join(p[0] for p in pats)
    return float(score), f"{names}", pats
