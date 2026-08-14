"""Politician / lawmaker stock activity — free, keyless.
Public House & Senate financial-disclosure datasets (Stock Watcher project).
We fold recent lawmaker BUYS/SELLS in as a small confirmation signal."""
import json, urllib.request
from datetime import datetime, timedelta

HOUSE_URL  = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
SENATE_URL = "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json"

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (St0ckMarken)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

def _parse_date(s):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"):
        try: return datetime.strptime(str(s)[:19], fmt)
        except Exception: continue
    return None

def recent_activity(days=90):
    """{TICKER: {'buys':int,'sells':int,'names':[..]}} from the last `days`."""
    out, cutoff = {}, datetime.today() - timedelta(days=days)
    for url in (HOUSE_URL, SENATE_URL):
        try:
            data = _get(url)
        except Exception:
            continue
        for tx in data:
            tkr = str(tx.get("ticker") or "").upper().strip()
            if not tkr or tkr in ("--", "N/A", "NONE"): continue
            d = _parse_date(tx.get("transaction_date") or tx.get("disclosure_date"))
            if d is None or d < cutoff: continue
            typ = str(tx.get("type") or tx.get("transaction_type") or "").lower()
            who = tx.get("representative") or tx.get("senator") or "a lawmaker"
            rec = out.setdefault(tkr, {"buys": 0, "sells": 0, "names": []})
            if "purch" in typ or typ == "buy":
                rec["buys"] += 1
                if who not in rec["names"]: rec["names"].append(who)
            elif "sale" in typ or "sold" in typ or typ == "sell":
                rec["sells"] += 1
    return out

def top_buys(activity, n=5):
    ranked = sorted(activity.items(), key=lambda kv: kv[1]["buys"] - kv[1]["sells"], reverse=True)
    return [(t, a["buys"], a["sells"], a["names"][:2]) for t, a in ranked if a["buys"] > a["sells"]][:n]

def follow_list(days=90, n=8):
    """Person-level 'real traders to follow': each recent BUY with who, what, when.
    Real named lawmakers + real public trades (STOCK Act disclosures). Keyless."""
    people, cutoff = [], datetime.today() - timedelta(days=days)
    seen = set()
    for url in (HOUSE_URL, SENATE_URL):
        try:
            data = _get(url)
        except Exception:
            continue
        for tx in data:
            tkr = str(tx.get("ticker") or "").upper().strip()
            if not tkr or tkr in ("--", "N/A", "NONE"): continue
            typ = str(tx.get("type") or tx.get("transaction_type") or "").lower()
            if not ("purch" in typ or typ == "buy"): continue
            d = _parse_date(tx.get("transaction_date") or tx.get("disclosure_date"))
            if d is None or d < cutoff: continue
            who = tx.get("representative") or tx.get("senator") or "A lawmaker"
            chamber = "Senator" if tx.get("senator") else "Representative"
            amt = str(tx.get("amount") or "").strip()
            key = (who, tkr)
            if key in seen: continue
            seen.add(key)
            people.append({"who": who, "role": chamber, "ticker": tkr,
                           "amount": amt, "date": d.strftime("%b %d, %Y"), "_d": d})
    people.sort(key=lambda p: p["_d"], reverse=True)
    for p in people: p.pop("_d", None)
    return people[:n]
