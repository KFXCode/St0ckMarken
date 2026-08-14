"""Pick logging + automatic outcome grading.
Every recommendation is appended to data/picks.csv; on each run, open picks past
their grade window are graded from the underlying's actual move (free data,
no broker needed):
  WIN  = underlying moved >= WIN_MOVE_PCT in our direction within the window
  LOSS = it didn't
  est. premium P/L% = underlying %move x (spot/premium) x DELTA_PROXY, capped at -100%
"""
import csv, os
from datetime import datetime
import pandas as pd
import yfinance as yf
from . import config as C

FIELDS = ["date","ticker","direction","kind","action","expiry","spot","strike","premium",
          "cost","conviction","status","graded_on","move_pct","est_pl_pct","result"]

def _load():
    if not os.path.exists(C.PICKS_LOG): return []
    with open(C.PICKS_LOG, newline="") as f:
        return list(csv.DictReader(f))

def _save(rows):
    os.makedirs(os.path.dirname(C.PICKS_LOG), exist_ok=True)
    with open(C.PICKS_LOG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

def log_picks(plays, run_date):
    rows = _load()
    seen = {(r["date"], r["ticker"]) for r in rows}
    for p in plays:
        key = (run_date, p["ticker"])
        if key in seen: continue
        rows.append({"date": run_date, "ticker": p["ticker"], "direction": p["direction"],
                     "kind": p["kind"], "action": p["action"], "expiry": p["expiry"],
                     "spot": p["spot"], "strike": p["strike"], "premium": p["premium"],
                     "cost": p["cost"], "conviction": p["conviction"], "status": "OPEN",
                     "graded_on": "", "move_pct": "", "est_pl_pct": "", "result": ""})
    _save(rows)
    return rows

def log_spot(spot_trades, run_date):
    """Log actionable crypto/forex/commodity/meme spot buys so they get graded too."""
    rows = _load()
    seen = {(r["date"], r["ticker"]) for r in rows}
    for w in spot_trades:
        key = (run_date, w["symbol"])
        if key in seen: continue
        rows.append({"date": run_date, "ticker": w["symbol"], "direction": w["direction"],
                     "kind": "SPOT", "action": "BUY", "expiry": "",
                     "spot": w["price"], "strike": 0, "premium": w["price"],
                     "cost": C.SPOT_POSITION_USD, "conviction": w.get("conv", ""), "status": "OPEN",
                     "graded_on": "", "move_pct": "", "est_pl_pct": "", "result": ""})
    _save(rows)
    return rows

def _grade_window(row):
    return C.GRADE_WINDOW_SPOT if row.get("kind") == "SPOT" else C.GRADE_WINDOW_DAYS

def grade_open_picks():
    rows = _load()
    today = pd.Timestamp.today().normalize()
    changed = False
    for r in rows:
        if r["status"] != "OPEN": continue
        opened = pd.Timestamp(r["date"])
        window = _grade_window(r)
        elapsed = len(pd.bdate_range(opened, today)) - 1
        try:
            hist = yf.download(r["ticker"], start=opened.strftime("%Y-%m-%d"),
                               progress=False, auto_adjust=True)["Close"].dropna()
            if hist.empty: continue
            entry = float(r["spot"])
            closes = hist.iloc[1:window + 1] if len(hist) > 1 else hist
            if len(closes) == 0: continue
            if r["direction"] == "BULLISH":
                best = float(closes.max()); best_move = (best / entry - 1) * 100
            else:
                best = float(closes.min()); best_move = (entry / best - 1) * 100
            hit_target = best_move >= C.WIN_MOVE_PCT
            window_done = elapsed >= window
            # Early-grade a winner as soon as it hits target; otherwise wait for the window.
            if not (hit_target and C.EARLY_GRADE) and not window_done:
                continue
            prem = float(r["premium"]) or 0.01
            final = float(closes.iloc[-1])
            if r["kind"] == "SPOT":
                move = best_move if hit_target else (final / entry - 1) * 100
                win = move >= C.WIN_MOVE_PCT
                est_pl = round(move, 1)
            elif r["kind"] == "CASH-SECURED PUT":
                win = final >= float(r["strike"]) or hit_target
                move = best_move
                est_pl = 100.0 if win else max(-100.0, (final - float(r["strike"])) / prem * 100)
            else:
                win = hit_target
                move = best_move if hit_target else (final / entry - 1) * 100 * (1 if r["direction"] == "BULLISH" else -1)
                leverage = entry / prem * C.DELTA_PROXY
                signed = move if win else -abs(move)
                est_pl = max(-100.0, round(signed / 100 * leverage * 100, 1))
            r.update({"status": "GRADED", "graded_on": today.strftime("%Y-%m-%d"),
                      "move_pct": round(move, 2), "est_pl_pct": round(float(est_pl), 1),
                      "result": "WIN" if win else "LOSS"})
            changed = True
        except Exception:
            continue
    if changed: _save(rows)
    return rows

def record_summary(rows):
    graded = [r for r in rows if r["status"] == "GRADED"]
    wins = sum(1 for r in graded if r["result"] == "WIN")
    losses = len(graded) - wins
    pl = [float(r["est_pl_pct"]) for r in graded if r["est_pl_pct"] != ""]
    cum, series = 0.0, []
    for r in sorted(graded, key=lambda x: x["graded_on"]):
        if r["est_pl_pct"] != "":
            cum += float(r["est_pl_pct"])
            series.append(round(cum, 1))
    since = min((r["date"] for r in rows), default=datetime.today().strftime("%Y-%m-%d"))
    return {"wins": wins, "losses": losses, "open": sum(1 for r in rows if r["status"] == "OPEN"),
            "total_pl": round(sum(pl), 1) if pl else 0.0, "series": series, "since": since}
