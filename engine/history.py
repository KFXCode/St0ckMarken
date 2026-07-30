"""Historical validation: backtests today's exact setup against years of past data,
plus monthly seasonality — so every trade card can show how this pattern actually
performed historically, not just today's signals."""
import numpy as np
import pandas as pd
import yfinance as yf
from . import config as C
from .signals import macd as macd_f, rsi as rsi_f

MONTHS = ["", "January","February","March","April","May","June","July",
          "August","September","October","November","December"]

def backtest_setup(ticker, direction, years=10):
    """Find every past day this ticker showed today's signal combination
    (trend direction + MACD side + RSI zone) and measure how often the stock
    then moved >= WIN_MOVE_PCT in our direction within the grade window.
    Returns dict or None if not enough history/occurrences."""
    try:
        df = yf.download(ticker, period=f"{years}y", interval="1d",
                         progress=False, auto_adjust=True)
        if df is None or len(df) < 300:
            return None
        c = df["Close"].squeeze().dropna()
        s20, s50 = c.rolling(20).mean(), c.rolling(50).mean()
        line, sig, _ = macd_f(c)
        r = rsi_f(c)
        bull = direction == "BULLISH"
        if bull:
            setup = (s20 > s50) & (line > sig) & r.between(45, 70)
        else:
            setup = (s20 < s50) & (line < sig) & r.between(30, 55)
        win_n = C.GRADE_WINDOW_DAYS
        mask = setup.fillna(False).values
        arr = c.values
        idx = [i for i in np.where(mask)[0] if i + win_n + 1 < len(arr)]
        if len(idx) < 20:
            return None
        wins, moves = 0, []
        for i in idx:
            entry = arr[i]
            fwd = arr[i + 1:i + 1 + win_n]
            best = fwd.max() if bull else fwd.min()
            move = (best / entry - 1) * 100 if bull else (entry / best - 1) * 100
            moves.append(move)
            if move >= C.WIN_MOVE_PCT:
                wins += 1
        hit = wins / len(idx) * 100
        # Monthly seasonality: average return for the current calendar month
        monthly = c.resample("ME").last().pct_change() * 100
        month = pd.Timestamp.today().month
        by_month = monthly.groupby(monthly.index.month).mean()
        sea = float(by_month.get(month, np.nan))
        span = round((c.index[-1] - c.index[0]).days / 365.25, 1)
        return {"n": len(idx), "hit": round(hit, 0), "avg": round(float(np.mean(moves)), 1),
                "years": span, "month": MONTHS[month],
                "sea": None if np.isnan(sea) else round(sea, 1)}
    except Exception:
        return None
