"""Strategy: composite scoring, edge gate, option-play construction."""
from datetime import datetime, timezone
import pandas as pd
from . import config as C
from . import signals as S
from . import data as D
from . import flavor as F
from . import candles as CD

def timeframe_for(expiry):
    """Label a trade by days-to-expiry: Day-swing / Swing / Long-term."""
    import pandas as pd
    dte = (pd.Timestamp(expiry) - pd.Timestamp.today().normalize()).days
    if dte <= 14: return "DAY / FAST SWING"
    if dte <= 45: return "SWING (days–weeks)"
    return "LONG-TERM (months)"

def composite_score(df, spy_df, news, flavor_pts, congress_act, social_bz, ticker):
    """Returns (direction_score 0-100, conviction 0-100, reasons list, extras)."""
    parts, reasons = {}, []
    parts["trend"], n = S.score_trend(df); reasons.append(("Trend", n, parts["trend"]))
    parts["candles"], n, patterns = CD.score_candles(df); reasons.append(("Candlestick", n, parts["candles"]))
    parts["rsi"], n = S.score_rsi(df); reasons.append(("RSI", n, parts["rsi"]))
    parts["macd"], n = S.score_macd(df); reasons.append(("MACD", n, parts["macd"]))
    parts["volume"], n, vol_ratio = S.score_volume(df); reasons.append(("Volume", n, parts["volume"]))
    parts["rel_str"], n = S.score_rel_strength(df, spy_df); reasons.append(("Rel. strength", n, parts["rel_str"]))
    parts["volatility"], n, hv_pctl = S.score_volatility(df); reasons.append(("Volatility", n, parts["volatility"]))
    parts["sentiment"], n = S.score_sentiment(news); reasons.append(("News", n, parts["sentiment"]))
    parts["congress"], n = S.score_congress(ticker, congress_act); reasons.append(("Elite flows", n, parts["congress"]))
    parts["social"], n = S.score_social(ticker, social_bz); reasons.append(("Social buzz", n, parts["social"]))
    parts["flavor"] = flavor_pts
    score = sum(parts[k] * C.WEIGHTS[k] for k in parts) / 100.0
    conviction = abs(score - 50) * 2
    return score, conviction, reasons, {"vol_ratio": vol_ratio, "hv_pctl": hv_pctl, "patterns": patterns}

def _pick_contract(chain, target_strike):
    if chain is None or chain.empty: return None
    ch = chain.copy()
    ch = ch[(ch["openInterest"].fillna(0) >= C.MIN_OPEN_INTEREST) & (ch["bid"].fillna(0) > 0)]
    if ch.empty: return None
    ch["dist"] = (ch["strike"] - target_strike).abs()
    row = ch.sort_values("dist").iloc[0]
    mid = (row["bid"] + row["ask"]) / 2
    if mid <= 0 or (row["ask"] - row["bid"]) / mid > C.MAX_SPREAD_PCT: return None
    return {"strike": float(row["strike"]), "bid": float(row["bid"]), "ask": float(row["ask"]),
            "mid": round(float(mid), 2), "oi": int(row["openInterest"]), "volume": int(row.get("volume") or 0)}

def build_play(ticker, score, conviction, reasons, extras, spot_hint=None):
    """Turn a graded candidate into a concrete options play, or None if no clean contract."""
    bullish = score >= 50
    expiry, calls, puts, spot = D.fetch_chain(ticker, C.DTE_MIN, C.DTE_MAX)
    if spot is None: spot = spot_hint
    if expiry is None or spot is None: return None
    hv_pctl = extras.get("hv_pctl")
    sell_premium = bullish and hv_pctl is not None and hv_pctl >= C.HIGH_IV_HV_PCTL

    if sell_premium:  # rich vol + bullish -> cash-secured put
        c = _pick_contract(puts, spot * (1 - C.CSP_OTM_PCT))
        if not c: return None
        kind, action = "CASH-SECURED PUT", "SELL"
        cost = c["strike"] * 100  # collateral
        budget_ok = False
        plain = (f"Sell the ${c['strike']:.0f} put expiring {expiry}. You collect ~${c['mid']*100:.0f} up front. "
                 f"Requires ${cost:,.0f} cash collateral — you're agreeing to buy 100 shares at ${c['strike']:.0f} if assigned.")
    elif bullish:
        c = _pick_contract(calls, spot * (1 + C.OTM_PCT_CALL))
        if not c: return None
        kind, action = "LONG CALL", "BUY"
        cost = c["ask"] * 100
        budget_ok = cost <= C.SMALL_ACCOUNT_BUDGET
        plain = (f"Buy the ${c['strike']:.0f} call expiring {expiry} for ~${c['ask']*100:.0f}. "
                 f"Max loss = what you pay. Profits if {ticker} rises meaningfully before expiry.")
    else:
        c = _pick_contract(puts, spot * (1 - C.OTM_PCT_PUT))
        if not c: return None
        kind, action = "LONG PUT", "BUY"
        cost = c["ask"] * 100
        budget_ok = cost <= C.SMALL_ACCOUNT_BUDGET
        plain = (f"Buy the ${c['strike']:.0f} put expiring {expiry} for ~${c['ask']*100:.0f}. "
                 f"Max loss = what you pay. Profits if {ticker} falls meaningfully before expiry.")

    return {"ticker": ticker, "direction": "BULLISH" if bullish else "BEARISH",
            "kind": kind, "action": action, "expiry": expiry, "spot": round(float(spot), 2),
            "strike": c["strike"], "premium": c["mid"], "ask": c["ask"], "oi": c["oi"],
            "cost": round(cost, 2), "budget_ok": budget_ok, "plain": plain,
            "score": round(score, 1), "conviction": round(conviction, 1),
            "reasons": reasons, "size": "1 position"}

def run_strategy(histories, spy_df, flavor_pts, flavor_notes, congress_act, social_bz):
    """Score the universe; return (plays, near_misses)."""
    graded = []
    for t, df in histories.items():
        if t == "SPY": continue
        try:
            news = D.fetch_news(t) if len(df) else []
            score, conv, reasons, extras = composite_score(df, spy_df, news, flavor_pts, congress_act, social_bz, t)
            graded.append((t, score, conv, reasons, extras, float(df["Close"].iloc[-1])))
        except Exception:
            continue
    # Focus on low-priced stocks: little money in, big % reward. Cheaper names first,
    # then by conviction (both still must clear the edge gate below).
    if C.PREFER_CHEAP:
        graded = [g for g in graded if g[5] <= C.MAX_UNDERLYING_PRICE] or graded
        graded.sort(key=lambda g: (g[2] >= C.MIN_CONVICTION, -g[5], g[2]), reverse=True)
    else:
        graded.sort(key=lambda g: g[2], reverse=True)

    plays, near = [], []
    for t, score, conv, reasons, extras, spot in graded:
        if conv >= C.MIN_CONVICTION and len(plays) < C.MAX_PICKS:
            p = build_play(t, score, conv, reasons, extras, spot_hint=spot)
            D.polite_pause()
            if p:
                p["reasons"] = p["reasons"] + [("Flavor", n, flavor_pts) for n in flavor_notes]
                p["timeframe"] = timeframe_for(p["expiry"])
                p["patterns"] = extras.get("patterns", [])
                plays.append(p)
        elif C.NEAR_MISS_BAND[0] <= conv < C.MIN_CONVICTION and len(near) < 6:
            weakest = min(reasons, key=lambda r: abs(r[2] - 50) if score >= 50 else -(r[2] - 50))
            blockers = [r for r in reasons if (r[2] < 45 if score >= 50 else r[2] > 55)]
            why = "; ".join(b[1] for b in blockers[:2]) or weakest[1]
            near.append({"ticker": t, "direction": "BULLISH" if score >= 50 else "BEARISH",
                         "conviction": round(conv, 1), "why_not": why})
    return plays, near
