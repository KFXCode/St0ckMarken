"""Social buzz + trending strategies — free, keyless stand-ins for X/Twitter.
NOTE: X/Twitter removed its free/keyless API and blocks scraping, so we use the
genuinely-free public JSON from StockTwits (trending tickers) and Reddit
(r/wallstreetbets, r/options, r/stocks mention counts + naive tone). Labeled
honestly in the report as 'retail social buzz', which is often a fade signal."""
import json, re, urllib.request
from collections import defaultdict

ST_TRENDING = "https://api.stocktwits.com/api/2/trending/symbols.json"
REDDIT = ["https://www.reddit.com/r/wallstreetbets/hot.json?limit=60",
          "https://www.reddit.com/r/options/hot.json?limit=40",
          "https://www.reddit.com/r/stocks/hot.json?limit=40"]

BULL = ("calls","long","buy","bull","moon","breakout","squeeze","rip","up","green")
BEAR = ("puts","short","sell","bear","crash","dump","down","red","drill","tank")

# Curated, human-vetted playbook of the high-engagement tactics circulating on
# trading X/Reddit — folded in as education, not auto-scraped signals.
STRATEGY_PLAYBOOK = [
    ("Day trade", "Opening Range Breakout (ORB) — mark the high/low of the first 5-30 minutes, then trade the breakout with volume confirmation. Repeatedly called one of the cleanest, most reliable day setups."),
    ("Day trade", "VWAP + 9/20 EMA pullbacks — on 5-10 min charts, buy retests in the direction of the trend. Strong on SPY/QQQ, often paired with ORB."),
    ("Swing", "Weekly trend + Optimal Trade Entry (Fib 62-79%) — trade with the weekly trend, enter on the pullback, target ~3R, and close if it takes longer than ~2 weeks."),
    ("Swing", "Momentum breakout after first consolidation — fresh trend with stacked 8/20/50 EMAs, buy the first clean pullback/consolidation breakout."),
    ("Swing", "200 SMA flip — price breaks above the daily 200 SMA and it turns from resistance into support. Simple continuation."),
    ("Rule", "Specialize in ONE setup and use strict risk (~1% or less per trade). High-signal accounts say this discipline IS the edge — swing traders generally out-earn pure day traders."),
]

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (St0ckMarken)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def buzz(universe):
    """{TICKER: {'mentions':int,'bull':int,'bear':int,'trending':bool}} for names in `universe`."""
    uni = set(universe)
    out = defaultdict(lambda: {"mentions": 0, "bull": 0, "bear": 0, "trending": False})
    try:
        for s in _get(ST_TRENDING).get("symbols", []):
            t = str(s.get("symbol", "")).upper()
            if t in uni:
                out[t]["trending"] = True
                out[t]["mentions"] += 3
    except Exception:
        pass
    tick_re = re.compile(r"\b([A-Z]{2,5})\b")
    for url in REDDIT:
        try:
            posts = _get(url)["data"]["children"]
        except Exception:
            continue
        for p in posts:
            d = p.get("data", {})
            title = (d.get("title") or "")
            low = title.lower()
            b = sum(w in low for w in BULL)
            s = sum(w in low for w in BEAR)
            for m in set(tick_re.findall(title.upper())):
                if m in uni:
                    out[m]["mentions"] += 1
                    out[m]["bull"] += b
                    out[m]["bear"] += s
    return dict(out)

def top_buzz(bz, n=5):
    ranked = sorted(bz.items(), key=lambda kv: kv[1]["mentions"], reverse=True)
    return [(t, v["mentions"], v["bull"], v["bear"], v["trending"]) for t, v in ranked if v["mentions"] > 0][:n]
