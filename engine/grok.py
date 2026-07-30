"""Optional Grok (xAI) layer — LIVE X/news for the final trades only.
Off automatically unless XAI_API_KEY is set (GitHub secret), so the pipeline
still runs 100% free without it. Called for the <=5 published trades only,
to keep cost to pennies per day.

Get a key at console.x.ai, add credits, then store it as the GitHub Actions
secret XAI_API_KEY. Nothing here places trades or touches your broker account."""
import os, json, urllib.request

API_URL = "https://api.x.ai/v1/chat/completions"
MODEL = os.environ.get("XAI_MODEL", "grok-3")

def enabled():
    return bool(os.environ.get("XAI_API_KEY"))

def _call(messages, max_tokens=500):
    key = os.environ.get("XAI_API_KEY")
    body = json.dumps({"model": MODEL, "messages": messages,
                       "temperature": 0.2, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = json.load(r)
    return data["choices"][0]["message"]["content"]

def analyze(ticker, direction, spot):
    """Live X + news read for one ticker. Returns dict or None on failure."""
    if not enabled():
        return None
    prompt = (
        f"You are a market analyst with live access to X (Twitter) and news. "
        f"For {ticker} (currently near ${spot}), our system has a {direction} bias. "
        f"Using the most recent posts from high-signal trading and politician-tracker "
        f"accounts and today's news, respond in STRICT JSON with keys: "
        f'"sentiment" (integer 0-100, 50=neutral, higher=more bullish), '
        f'"headlines" (array of up to 3 short factual strings, each with a rough date), '
        f'"take" (one plain-English sentence a beginner can understand on whether live '
        f"chatter agrees or disagrees with the {direction} bias). "
        f"Only output the JSON object, nothing else."
    )
    try:
        raw = _call([{"role": "user", "content": prompt}])
        raw = raw.strip().strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
        d = json.loads(raw)
        s = int(d.get("sentiment", 50))
        return {"sentiment": max(0, min(100, s)),
                "headlines": [str(h) for h in (d.get("headlines") or [])][:3],
                "take": str(d.get("take", "")).strip()}
    except Exception:
        return None
