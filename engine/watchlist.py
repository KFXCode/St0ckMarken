"""Other-markets watchlist scan — crypto, forex, commodities, meme coins.
These don't have Yahoo options chains, so we score them for a simple spot
(buy-the-thing) lean using trend + candlesticks, and present them as watch
cards. Fully defensive: any symbol that fails is skipped."""
import time
import yfinance as yf
from . import config as C
from . import candles as CD
from . import social as SO
from .signals import score_trend

def _download(sym, tries=3):
    """Resilient single-symbol daily download with retry + polite pause."""
    for i in range(tries):
        try:
            df = yf.download(sym, period="6mo", interval="1d",
                             progress=False, auto_adjust=True, threads=False)
            if df is not None and len(df) >= 30:
                if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
                    df.columns = df.columns.get_level_values(0)
                return df.dropna()
        except Exception:
            pass
        time.sleep(1.2 * (i + 1))  # back off, then retry
    return None

def _download_batch(syms):
    """One batched request for the whole class (far less rate-limiting than N calls),
    with a per-symbol retry fallback for anything the batch missed."""
    out = {}
    try:
        data = yf.download(syms, period="6mo", interval="1d", group_by="ticker",
                           auto_adjust=True, progress=False, threads=True)
        multi = hasattr(data.columns, "nlevels") and data.columns.nlevels > 1
        for s in syms:
            try:
                df = (data[s] if multi else data).dropna()
                if len(df) >= 30:
                    out[s] = df
            except Exception:
                pass
    except Exception:
        pass
    for s in syms:                      # fallback for any that didn't come back
        if s not in out:
            time.sleep(0.6)
            df = _download(s)
            if df is not None:
                out[s] = df
    return out

def _scan(pairs):
    # Same social layer as stocks: Reddit (WSB/options/stocks) + StockTwits buzz,
    # matched on the ticker base (e.g. DOGE, BTC, PEPE). Free, keyless.
    bases = [sym.replace("-USD", "").replace("=F", "").replace("=X", "") for sym, _ in pairs]
    try:
        bz = SO.buzz(bases)
    except Exception:
        bz = {}
    hist = _download_batch([sym for sym, _ in pairs])
    out = []
    for sym, name in pairs:
        try:
            df = hist.get(sym)
            if df is None:
                continue
            price = float(df["Close"].iloc[-1])
            wk = df["Close"].iloc[-6] if len(df) > 6 else df["Close"].iloc[0]
            chg = (price / float(wk) - 1) * 100
            tscore, tnote = score_trend(df)
            cscore, cnote, pats = CD.score_candles(df)
            score = (tscore + cscore) / 2
            base = sym.replace("-USD", "").replace("=F", "").replace("=X", "")
            ssc, snote = SO.score_social(base, bz)
            if base in (bz or {}):
                score = score * 0.85 + ssc * 0.15
                tnote = f"{tnote}; social: {snote}"
            direction = "BULLISH" if score >= 50 else "BEARISH"
            conv = abs(score - 50) * 2
            is_trade = conv >= C.WATCH_TRADE_CONV and direction == "BULLISH"
            pat_txt = pats[0][2] if pats else "no clear candlestick signal on the latest bar"
            out.append({"symbol": sym, "name": name, "price": price, "chg": round(chg, 1),
                        "direction": direction, "score": round(score, 0), "conv": round(conv, 0),
                        "is_trade": bool(is_trade), "suggest": "BUY" if is_trade else "WATCH",
                        "trend": tnote, "pattern": pat_txt,
                        "pattern_name": pats[0][0] if pats else ""})
        except Exception:
            continue
        finally:
            pass
    out.sort(key=lambda x: abs(x["score"] - 50), reverse=True)
    return out[:C.WATCH_TOP]

def scan_watchlist():
    return {cls: _scan(pairs) for cls, pairs in C.WATCHLIST.items()}

def scan_meme():
    return _scan(C.MEME_WATCH)
