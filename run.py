"""Daily pipeline entrypoint: fetch -> grade -> score -> pick -> track -> report."""
import os
from datetime import datetime, timezone, timedelta
import pandas as pd
from engine import (config as C, data as D, flavor as F, history as H,
                    congress as CG, social as SO, grok as GK, watchlist as WL,
                    strategy, tracker, report)

def main():
    now = datetime.now(timezone.utc)
    est = now - timedelta(hours=4)
    date_str = est.strftime("%Y-%m-%d")
    updated = est.strftime("%b %d, %Y - %I:%M %p EDT")
    is_weekend = est.weekday() >= 5  # Sat=5, Sun=6 — US stock market closed
    warnings = []

    print("1/7 grading prior picks...")
    tracker.grade_open_picks()

    print("2/7 downloading history for", len(C.UNIVERSE), "tickers...")
    universe = [t for t in C.UNIVERSE if t not in C.ROBINHOOD_UNSUPPORTED]
    hist = D.fetch_history(universe)
    if "SPY" not in hist:
        raise SystemExit("SPY history unavailable — aborting run")
    if len(hist) < len(C.UNIVERSE) * 0.7:
        warnings.append(f"Only {len(hist)}/{len(C.UNIVERSE)} tickers returned usable history from Yahoo today.")

    print("3/7 market snapshot...")
    spy = hist["SPY"]
    vix_df = D.fetch_history(["^VIX"], period="1mo")
    vix = round(float(vix_df["^VIX"]["Close"].iloc[-1]), 1) if "^VIX" in vix_df else "n/a"
    market = {"spy": round(float(spy["Close"].iloc[-1]), 2),
              "spy_chg": float((spy["Close"].iloc[-1] / spy["Close"].iloc[-2] - 1) * 100),
              "vix": vix, "scanned": len(hist)}

    flavor_pts, flavor_notes, flavor_meta = F.flavor_score(now)

    print("4/7 elite flows (Congress) + social buzz...")
    try:
        congress_act = CG.recent_activity()
    except Exception:
        congress_act = {}
    if not congress_act:
        warnings.append("Congressional-disclosure feed was unavailable today — elite-flows factor scored neutral.")
    try:
        social_bz = SO.buzz(C.UNIVERSE)
    except Exception:
        social_bz = {}
    congress_top = CG.top_buys(congress_act)
    social_top = SO.top_buzz(social_bz)

    print("4b/7 scoring universe + building trades...")
    beginner, experienced = strategy.run_strategy(hist, spy, flavor_pts, flavor_notes, congress_act, social_bz)
    plays = beginner + experienced

    if GK.enabled():
        print("4c/7 Grok live X/news read on final trades...")
        for p in plays:
            g = GK.analyze(p["ticker"], p["direction"], p["spot"])
            if g:
                p["grok"] = g
                p["reasons"] = p["reasons"] + [("Grok live X", g["take"] or "live read attached", g["sentiment"])]

    print("5/7 historical backtest of each setup...")
    for p in plays:
        p["history"] = H.backtest_setup(p["ticker"], p["direction"])
        D.polite_pause()

    print("6/7 earnings check + logging...")
    earnings_warnings = []
    week_end = pd.Timestamp.today() + pd.Timedelta(days=7)
    for p in plays:
        ed = D.fetch_earnings_date(p["ticker"])
        D.polite_pause()
        if ed is None:
            continue
        ed = ed.tz_localize(None) if ed.tzinfo else ed
        if pd.Timestamp.today().normalize() <= ed <= week_end:
            earnings_warnings.append(f"{p['ticker']} reports earnings {ed.strftime('%b %d')} — big-move risk in either direction.")
    rows = tracker.log_picks(plays, date_str)

    print("7/7 other markets (crypto/forex/commodities/meme)...")
    try:
        watch = WL.scan_watchlist()
    except Exception:
        watch = {}
    try:
        meme = WL.scan_meme()
    except Exception:
        meme = []
    spot_trades = [w for lst in watch.values() for w in lst if w.get("is_trade")]
    spot_trades += [w for w in meme if w.get("is_trade")]
    if spot_trades:
        rows = tracker.log_spot(spot_trades, date_str)
    record = tracker.record_summary(rows)

    html_out = report.render(date_str, updated, beginner, experienced, record, flavor_meta,
                             market, earnings_warnings, warnings, picks_rows=rows,
                             congress_top=congress_top, social_top=social_top,
                             playbook=SO.STRATEGY_PLAYBOOK, grok_on=GK.enabled(),
                             watch=watch, meme=meme, is_weekend=is_weekend)
    os.makedirs(os.path.dirname(C.REPORT_PATH), exist_ok=True)
    with open(C.REPORT_PATH, "w") as f:
        f.write(html_out)
    print(f"done: {len(beginner)} beginner + {len(experienced)} experienced -> {C.REPORT_PATH}")

if __name__ == "__main__":
    main()
