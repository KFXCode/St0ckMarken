"""Dark, mobile-first HTML report — same style family as the MLB betting report."""
import html, json
from . import config as C

CSS = """
:root{--bg:#0e1420;--card:#17202f;--card2:#1e2a3c;--line:#293a52;--txt:#e9edf4;--dim:#93a1b8;
--green:#34d399;--red:#fb7185;--gold:#f5b84c;--blue:#7aa5f8;--purple:#b79df5}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font:16px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
padding:0 0 40px;max-width:520px;margin:0 auto}
.wrap{padding:14px}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);z-index:5}
.brand{font-size:18px;font-weight:800;letter-spacing:-.02em}
.brand span{color:var(--green)}
.hero{padding:18px 16px 6px}
.hero .pv{font-size:38px;font-weight:800;letter-spacing:-.03em}
.hero .pc{font-size:15px;font-weight:600;margin-top:2px}
.hero .pl{font-size:13px;color:var(--dim);margin-top:2px}
a{color:var(--blue)} a:hover{color:#93c5fd}
h1{font-size:26px;margin:6px 0 2px} .sub{color:var(--dim);font-size:14px}
.meta{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:14px 0;font-size:14px}
.meta b{color:var(--gold)}
.warn{background:#261e10;border:1px solid #4d3d18;border-radius:12px;padding:12px 14px;margin:14px 0;font-size:13.5px;color:#eec877}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0}
.playtag{font-size:12px;letter-spacing:.12em;color:var(--dim);text-transform:uppercase}
.title{font-size:21px;font-weight:700;margin:4px 0 2px}
.dir-b{color:var(--green)} .dir-s{color:var(--red)}
.stats{display:flex;gap:8px;margin:12px 0}
.stat{flex:1;background:var(--card2);border-radius:10px;padding:10px 6px;text-align:center}
.stat .v{font-size:19px;font-weight:700} .stat .l{font-size:11px;color:var(--dim);text-transform:uppercase;letter-spacing:.06em}
.plain{background:#0f2620;border:1px solid #1f4a3a;border-radius:10px;padding:11px 13px;font-size:14px;margin:12px 0}
.plain.bear{background:#271620;border-color:#4a2635}
ul{margin:8px 0 0 18px;font-size:14px;color:#c6cdd8} li{margin:4px 0}
.why{font-size:14px;font-weight:600;margin-top:12px}
.tagrow{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.tag{font-size:12px;padding:3px 10px;border-radius:99px;background:var(--card2);border:1px solid var(--line);color:var(--dim)}
.tag.good{color:var(--green);border-color:#1f4a3a}
.avoid{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:10px 0;font-size:14px}
.avoid b{font-size:15px}
.record{display:flex;gap:8px;margin:16px 0}
h2{font-size:18px;margin:26px 0 6px} .hint{color:var(--dim);font-size:13px}
.chart{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin:14px 0}
.foot{color:var(--dim);font-size:12.5px;text-align:center;margin-top:30px;line-height:1.7}
.disc{background:#271620;border:1px solid #4a2635;border-radius:12px;padding:12px 14px;margin:20px 0;font-size:13px;color:#eeadbe}
button{cursor:pointer;font-family:inherit}
.take{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:12px;border-top:1px solid var(--line);padding-top:12px}
.tbtn{width:32px;height:32px;border-radius:8px;background:var(--card2);border:1px solid var(--line);color:var(--txt);font-size:17px}
.tq{min-width:22px;text-align:center;font-weight:700}
.takebtn{background:#1f4a3a;border:1px solid #2c6a52;color:#7de8bb;border-radius:8px;padding:7px 14px;font-size:14px;font-weight:600}
.takebtn:disabled{opacity:.55;cursor:default}
.pot{font-size:12.5px;color:var(--dim);width:100%}
.pos{background:var(--card2);border-radius:8px;padding:8px 10px;margin:6px 0;font-size:14px}
#sm-amt{flex:1;min-width:0;background:var(--card2);border:1px solid var(--line);border-radius:8px;padding:9px 12px;color:var(--txt);font-size:16px}
.linkbtn{background:none;border:none;color:var(--dim);font-size:12.5px;text-decoration:underline;margin-top:10px;padding:0}
.guide{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:4px 16px;margin:16px 0}
.guide summary{font-size:15px;font-weight:700;padding:12px 0;cursor:pointer;color:#7de8bb}
.gsec{font-size:14px;color:#c6cdd8;margin:0 0 14px;line-height:1.6}
.gsec b{color:var(--txt)}
.flow{background:#101d17;border:1px solid #234032;border-radius:12px;padding:12px 14px;margin:10px 0;font-size:14px}
.flow b{color:#7de8bb}
.buzz{background:#1a1526;border:1px solid #3a2f52;border-radius:12px;padding:12px 14px;margin:10px 0;font-size:14px}
.buzz b{color:#c3aef0}
.pill{display:inline-block;font-size:12px;padding:2px 9px;border-radius:99px;background:var(--card2);border:1px solid var(--line);color:var(--dim);margin:3px 4px 0 0}
.cndl{background:#0d1a26;border:1px solid #1d3a52;border-radius:10px;padding:11px 13px;font-size:13.5px;margin:12px 0;color:#a9d2ec}
.cndl b{color:#7ec8f5}
.grok{background:#12140f;border:1px solid #2c3320;border-radius:10px;padding:11px 13px;font-size:13.5px;margin:12px 0;color:#c9d6b5}
.grok b{color:var(--green)}
.grow{background:#0f2620;border:1px solid #1f4a3a;border-radius:10px;padding:11px 13px;font-size:13.5px;margin:12px 0;color:#a9dcc3}
.grow b{color:#7de8bb}
.hist{background:#1d1a2e;border:1px solid #3a3260;border-radius:10px;padding:11px 13px;font-size:13.5px;margin:12px 0;color:#c9c2ea}
.brokerbtn{background:#1b2c4a;border:1px solid #2c4468;color:#9ec1f0;border-radius:8px;padding:7px 14px;font-size:14px;font-weight:600}
.scn{display:flex;justify-content:space-between;font-size:12.5px;color:var(--dim);padding:2.5px 0;border-bottom:1px dashed #223044}
.scn:last-child{border-bottom:none}
.scn-h{color:var(--txt);font-weight:600}
#sm-broker{background:var(--card2);border:1px solid var(--line);border-radius:8px;padding:8px 10px;color:var(--txt);font-size:14px;flex:1;min-width:0}
"""

GUIDE = """
<details class="guide" open>
<summary>👋 How to use this app (read me first!)</summary>
<div class="gsec"><b>What this app is.</b> Every morning a robot looks at hundreds of stocks and picks a few really good ones it thinks will go up (or down). It shows you exactly what to buy. Your job is just to copy the trade. Easy!</div>
<div class="gsec"><b>Step 1 — put in your money amount.</b> Scroll to <b>My Budget</b> and type how much you're starting with (even $20 is fine). Tap <b>Start</b>. This is pretend money at first, so you can practice with zero risk.</div>
<div class="gsec"><b>Step 2 — pick a trade.</b> Each <b>green card</b> is one trade idea. Look for the green <b>$100-friendly ✓</b> tag — those are cheap enough for a small budget. Read the <b>"In plain English"</b> box to see what it does.</div>
<div class="gsec"><b>Step 3 — see how much you could make.</b> The <b>"How your money can grow"</b> box shows what happens if the stock goes up… and the most you could lose (never more than what you pay). The blue box shows the <b>chart shapes</b> the robot spotted and why they matter.</div>
<div class="gsec"><b>Step 4 — take the trade.</b> Pick how many contracts with the <b>−</b> and <b>+</b> buttons, then tap <b>Take this trade</b> to add it to your practice money. Ready for real? Tap <b>Open in Robinhood</b> — it copies the order so you just paste and press buy in your Robinhood app.</div>
<div class="gsec"><b>Step 5 — watch it grow.</b> After a trade finishes, the app grades it a WIN or LOSS and updates your money. The <b>📈 Weekly Progress</b> section shows your money getting bigger week by week. Set a <b>🎯 weekly goal</b> and it tells you the honest truth about what's possible.</div>
<div class="gsec"><b>⭐ Golden rules.</b> 1) Only use money you're okay losing. 2) Start with the cheap trades. 3) Nothing sells by itself — you must tap <b>Sell to Close</b> in Robinhood to keep your profit. 4) Slow and steady wins — small wins stack up into big money over time.</div>
</details>
<details class="guide">
<summary>📗 New to options? Start here — the plain-English guide</summary>
<div class="gsec"><b>What you're actually buying.</b> A <b>call</b> is like a coupon: it gives you the right to buy 100 shares at a set price (the <b>strike</b>) until a set date (the <b>expiration</b>). A <b>put</b> is the same but for selling — it gains value when the stock FALLS. The price of the coupon itself is the <b>premium</b>. Premium $0.82 = one contract costs $82 (× 100 shares). You never have to actually buy the 100 shares — almost everyone just sells the coupon itself once it's worth more.</div>
<div class="gsec"><b>Step 0 — turn on options at your broker (one time).</b> Every app makes you enable options first: find <i>Settings → Options Trading → Enable</i> (Robinhood, Webull) or apply for "options approval" (Fidelity, Schwab). They ask a few questions about experience and income — answer honestly; <b>"Level 1–2" approval is all you need</b> to buy calls and puts. Approval usually takes minutes to a day.</div>
<div class="gsec"><b>Step-by-step: placing a pick from this report.</b><br>
1. Open your broker and search the ticker (e.g. SOFI).<br>
2. Tap <i>Trade → Options</i> (not the regular Buy button — that buys shares).<br>
3. Pick the <b>expiration date</b> shown on the card.<br>
4. Scroll the strike list to the <b>strike</b> on the card. Calls and puts are separate tabs — make sure you're on the right one.<br>
5. Choose <b>Buy to Open</b>, quantity <b>1 contract</b>.<br>
6. Set a <b>limit price</b> at (or a couple cents above) the premium on the card — never use a market order on options.<br>
7. Review: the cost should match the card (premium × 100). Submit.</div>
<div class="gsec"><b>⚠️ It does NOT sell itself.</b> If the premium rises, nothing happens automatically — the profit is only yours when you tap <b>Sell to Close</b> on that contract. If you never sell: the option loses a little value every single day (<b>time decay</b>), a paper profit can melt back to zero, and at expiration an out-of-the-money option becomes worthless — you lose the whole premium. (If it finishes IN the money, most brokers auto-sell or auto-exercise it on expiration day, but never rely on that — sell it yourself before expiry week.)</div>
<div class="gsec"><b>A simple exit plan (what most disciplined traders do).</b> Decide before you buy: take profit by selling at +50% to +100%; cut the loss by selling at −50%; and no matter what, be out at least a week before expiration, when time decay is fastest.</div>
<div class="gsec"><b>Why the engine picked these.</b> Every night it scans ~100 liquid stocks, and only shows a trade when trend, momentum (RSI/MACD), volume, and strength vs the market all point the same way — then it backtests that exact setup on up to 10 years of history (the purple box) to show how often it actually worked. If nothing clears the bar, it shows nothing. Staying in cash is a position.</div>
</details>"""

def _spark(series):
    if len(series) < 2:
        return '<div class="hint">Chart appears once at least two picks are graded.</div>'
    w, h = 560, 120
    lo, hi = min(series + [0]), max(series + [0])
    rng = (hi - lo) or 1
    pts = " ".join(f"{i*(w/(len(series)-1)):.1f},{h-(v-lo)/rng*h:.1f}" for i, v in enumerate(series))
    zero_y = h - (0 - lo) / rng * h
    color = "#34d399" if series[-1] >= 0 else "#fb7185"
    return (f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto">'
            f'<line x1="0" y1="{zero_y:.1f}" x2="{w}" y2="{zero_y:.1f}" stroke="#293a52" stroke-dasharray="4 4"/>'
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round"/></svg>')

def render(date_str, updated_str, plays, near_misses, record, flavor_meta,
           market, earnings_warnings, warnings, picks_rows=None,
           congress_top=None, social_top=None, playbook=None, grok_on=False):
    e = html.escape
    parts = [f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0e1420"><meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="St0ckMarken">
<title>St0ckMarken — {e(date_str)}</title><style>{CSS}</style></head><body>
<div class="topbar"><div class="brand">St0ck<span>Marken</span></div>
<div class="pl" style="color:var(--dim);font-size:12px">{e(date_str)}</div></div>
<div class="hero"><div class="pl">Your paper portfolio</div>
<div class="pv" id="sm-hero-pv">Set a budget ↓</div>
<div class="pc" id="sm-hero-pc"></div>
<div class="pl">SPY {market['spy']} ({market['spy_chg']:+.1f}%) · VIX {market['vix']} · {len(plays)} trades today</div></div>
<div class="wrap">
<div class="meta">Market: SPY <b>{market['spy']}</b> ({market['spy_chg']:+.1f}%) · VIX <b>{market['vix']}</b><br>
Scanned: <b>{market['scanned']} tickers</b> · Cleared the bar: <b>{len(plays)}</b><br>
Moon: <b>{e(flavor_meta['phase'])}</b> in <b>{e(flavor_meta['sign'])}</b> · Numerology: <b>{flavor_meta['numerology']}</b>
<span class="hint">(flavor layer, {C.WEIGHTS['flavor']}% weight)</span></div>"""]
    parts.append(GUIDE)
    for wtxt in warnings:
        parts.append(f'<div class="warn"><b>Data quality warning</b><br>{e(wtxt)}</div>')
    if earnings_warnings:
        items = "".join(f"<li>{e(x)}</li>" for x in earnings_warnings)
        parts.append(f'<div class="warn"><b>Earnings this week — extra risk</b><ul>{items}</ul></div>')
    if not plays:
        parts.append('<div class="card"><div class="title">No trades today</div>'
                     '<div class="hint">Nothing cleared the conservative edge threshold '
                     f'({C.MIN_CONVICTION:.0f}+ conviction). No filler trades, ever — staying in cash IS a position.</div></div>')
    for i, p in enumerate(plays, 1):
        dircls = "dir-b" if p["direction"] == "BULLISH" else "dir-s"
        bearcls = "" if p["direction"] == "BULLISH" else " bear"
        reasons = "".join(f"<li><b>{e(k)}:</b> {e(n)}</li>" for k, n, _ in p["reasons"])
        pats = p.get("patterns") or []
        if pats:
            lis = "".join(f'<li><b>{e(nm)}</b> ({"bullish" if d=="bull" else "bearish"}): {e(pl)}</li>' for nm, d, pl in pats)
            cndl_html = f'<div class="cndl"><b>📊 Chart patterns spotted (from the Candlestick Bible):</b><ul>{lis}</ul></div>'
        else:
            cndl_html = ''
        gk = p.get("grok")
        if gk:
            heads = "".join(f'<li>{e(x)}</li>' for x in gk.get("headlines", []))
            grok_html = (f'<div class="grok"><b>𝕏 Grok live read:</b> {e(gk.get("take",""))}'
                         + (f'<ul>{heads}</ul>' if heads else '') + '</div>')
        else:
            grok_html = ''
        h = p.get("history")
        if h:
            sea = f" {h['month']} has averaged {h['sea']:+.1f}% for {e(p['ticker'])} historically." if h.get("sea") is not None else ""
            hist_html = (f'<div class="hist"><b>History check ({h["years"]:g} yrs of data):</b> this exact signal setup '
                         f'appeared <b>{h["n"]}</b> times; the stock moved ≥{C.WIN_MOVE_PCT:g}% in this direction within '
                         f'{C.GRADE_WINDOW_DAYS} trading days <b>{h["hit"]:.0f}%</b> of the time (avg best move {h["avg"]:+.1f}%).{sea}</div>')
        else:
            hist_html = '<div class="hist"><b>History check:</b> not enough past occurrences of this setup to backtest — treat with extra caution.</div>'
        if p["kind"] == "CASH-SECURED PUT":
            grow_html = (f'<div class="grow"><b>How the money works here:</b> you set aside ${p["strike"]*100:,.0f} as collateral and '
                         f'collect ~${p["premium"]*100:,.0f} up front — that premium is the most you can make, and you keep it if '
                         f'{e(p["ticker"])} stays above ${p["strike"]:.0f}. <b>Can you lose more?</b> Yes, this one is different: if the stock '
                         f'drops below ${p["strike"]:.0f} you must buy 100 shares there, so losses grow the further it falls (worst case, '
                         f'stock to $0 = −${p["strike"]*100 - p["premium"]*100:,.0f}). That is why it needs the full collateral.</div>')
        else:
            c2, c5 = p["cost"] * 2, p["cost"] * 5
            grow_html = (f'<div class="grow"><b>How your money can grow:</b> you pay ~${p["cost"]:,.0f} once (the ${p["premium"]:.2f} premium '
                         f'× 100 shares) — and that is your entire risk. The contract itself trades, and its price moves several times faster '
                         f'than the stock. If the premium doubles to ${p["premium"]*2:.2f}, your ${p["cost"]:,.0f} becomes ${c2:,.0f} (+100%). '
                         f'On a big move past the ${p["strike"]:.0f} strike it could reach ${p["premium"]*5:.2f}, turning ${p["cost"]:,.0f} into '
                         f'${c5:,.0f} (+400%). <b>Can you lose more than ${p["cost"]:,.0f}?</b> No — when you BUY a call or put, your loss is capped '
                         f'at exactly what you paid; worst case it expires worthless. <b>Can you gain more than you paid?</b> Yes — the upside is uncapped. <b>One more thing:</b> profits are NOT taken automatically — you must tap "Sell to Close" at your broker to lock them in before expiration (full walkthrough in the beginner guide up top).</div>')
        budget = '<span class="tag good">$100-friendly ✓</span>' if p["budget_ok"] else \
                 f'<span class="tag">needs ~${p["cost"]:,.0f}</span>'
        parts.append(f"""<div class="card" data-screen-label="Trade {i}">
<div class="playtag">Trade #{i} · {e(p.get('timeframe','SWING'))} · {e(p['size'])}</div>
<div class="title">{e(p['ticker'])} <span class="{dircls}">{e(p['kind'])}</span></div>
<div class="sub">{e(p['action'])} the ${p['strike']:.0f} strike · expires {e(p['expiry'])} · stock at ${p['spot']:.2f}</div>
<div class="stats">
<div class="stat"><div class="v">{p['conviction']:.0f}</div><div class="l">Conviction</div></div>
<div class="stat"><div class="v">{p['score']:.0f}</div><div class="l">Score /100</div></div>
<div class="stat"><div class="v">${p['premium']:.2f}</div><div class="l">Premium</div></div>
</div>
<div class="plain{bearcls}"><b>In plain English:</b> {e(p['plain'])}</div>{grow_html}{cndl_html}{grok_html}{hist_html}
<div class="why">Why this trade sets up:</div><ul>{reasons}</ul>
<div class="tagrow">{budget}<span class="tag">OI {p['oi']:,}</span><span class="tag">{e(p['direction'].title())}</span></div>
<div class="take" data-t="{e(p['ticker'])}" data-date="{e(date_str)}" data-cost="{p['cost']}" data-prem="{p['premium']}" data-spot="{p['spot']}" data-kind="{e(p['kind'])}" data-strike="{p['strike']:.0f}" data-exp="{e(p['expiry'])}" data-action="{e(p['action'])}">
<button class="tbtn" data-d="-1">−</button><span class="tq">1</span><button class="tbtn" data-d="1">+</button>
<span class="hint">contracts</span><button class="takebtn">Take this trade</button><button class="brokerbtn">Open in broker</button>
<div class="pot"></div></div>
</div>""")
    if near_misses:
        parts.append('<h2>Why NOT to trade these</h2><div class="hint">Tempting on the surface, but they don\'t clear the bar:</div>')
        for n in near_misses:
            parts.append(f'<div class="avoid"><b>{e(n["ticker"])}</b> — looked {e(n["direction"].lower())} '
                         f'(conviction {n["conviction"]:.0f}, needs {C.MIN_CONVICTION:.0f}+)<br>'
                         f'<span class="hint">{e(n["why_not"])}</span></div>')
    if congress_top:
        rows = "".join(
            f'<div class="pill">{e(t)} · {b} buys{("/"+str(s)+" sells") if s else ""}'
            + (f' · {e(names[0])}' if names else "") + '</div>'
            for t, b, s, names in congress_top)
        parts.append(f'<h2>Elite Flows Watch</h2><div class="hint">What lawmakers have been buying recently '
                     f'(free House/Senate disclosures). A confirmation layer, not a trigger.</div>'
                     f'<div class="flow"><b>Recent lawmaker buys:</b><br>{rows}</div>')
    else:
        parts.append('<h2>Elite Flows Watch</h2><div class="flow"><b>No fresh lawmaker buys on file</b> '
                     '<span class="hint">(or the disclosure feed was quiet/unavailable today).</span></div>')
    if social_top:
        rows = "".join(
            f'<div class="pill">{e(t)} · {m} mentions{" · trending" if tr else ""}</div>'
            for t, m, bl, be, tr in social_top)
        parts.append(f'<h2>Social Buzz</h2><div class="hint">Loudest retail chatter on StockTwits / Reddit. '
                     f'X/Twitter has no free API, so these are the free stand-ins. Heavy hype is often a <i>fade</i> — '
                     f'we weight this small.</div><div class="buzz"><b>Most talked-about:</b><br>{rows}</div>')
    if playbook:
        items = "".join(f'<li><b>{e(tf)}:</b> {e(desc)}</li>' for tf, desc in playbook)
        parts.append(f'<div class="buzz"><b>Proven strategy playbook</b> '
                     f'<span class="hint">(vetted tactics circulating on trading X/Reddit, folded in as education)</span>'
                     f'<ul>{items}</ul></div>')
    parts.append('<div class="hint" style="margin:10px 0">'
                 + ('𝕏 Grok live X/news read is <b style="color:var(--green)">ON</b> for today\'s trades.' if grok_on
                    else 'Grok live-X layer is off (add an XAI_API_KEY secret to enable). Using free news + StockTwits/Reddit.')
                 + '</div>')
    parts.append("""<h2>My Budget</h2>
<div class="hint">Simulated bankroll — stored only in your browser. Set a budget, tap "Take this trade" on picks you'd play, and it grows or shrinks automatically as picks get graded.</div>
<div class="card" id="sm-budget">
<div id="sm-setup">
<div class="title" style="font-size:17px">Set your starting budget</div>
<div class="hint">Any amount — even $20 works. Nothing leaves your device.</div><div class="hint" style="margin-top:8px">💡 <b>Starting with $20?</b> Look for the green <b>$100-friendly ✓</b> trades — many cost under $20 for one contract. Buy ONE, let it work, and grow from there. You can never lose more than what one contract costs.</div>
<div style="display:flex;gap:8px;margin-top:10px">
<input id="sm-amt" type="number" min="1" inputmode="decimal" placeholder="e.g. 100">
<button class="takebtn" id="sm-start-btn">Start</button>
</div></div>
<div id="sm-dash" style="display:none">
<div class="stats">
<div class="stat"><div class="v" id="sm-v-start">$0</div><div class="l">Started</div></div>
<div class="stat"><div class="v" id="sm-v-now">$0</div><div class="l">Now</div></div>
<div class="stat"><div class="v" id="sm-v-gr">0%</div><div class="l">Growth</div></div>
</div>
<div class="hint" id="sm-cash"></div>
<div style="border-top:1px solid var(--line);margin-top:14px;padding-top:12px">
<div class="why" style="margin-top:0">🎯 My weekly goal</div>
<div style="display:flex;gap:8px;align-items:center;margin-top:8px">
<span class="hint" style="white-space:nowrap">Make per week:</span>
<input id="sm-goal" type="number" min="1" inputmode="decimal" placeholder="e.g. 100" style="flex:1;min-width:0;background:var(--card2);border:1px solid var(--line);border-radius:8px;padding:8px 10px;color:var(--txt);font-size:15px">
</div>
<div id="sm-goal-out" style="margin-top:10px"><span class="hint">Type a weekly $ goal above to see the honest math.</span></div>
</div>
<div id="sm-open"></div><div id="sm-closed"></div>
<div id="sm-weekly" style="border-top:1px solid var(--line);margin-top:14px;padding-top:12px"></div>
<button class="linkbtn" id="sm-reset">Reset budget tracker</button>
</div>
<div style="display:flex;gap:8px;align-items:center;margin-top:14px;border-top:1px solid var(--line);padding-top:12px">
<span class="hint" style="white-space:nowrap">Your broker:</span>
<select id="sm-broker"><option value="">choose…</option><option value="robinhood" selected>Robinhood</option><option value="webull">Webull</option><option value="fidelity">Fidelity</option><option value="schwab">Charles Schwab</option><option value="thinkorswim">thinkorswim</option><option value="etrade">E*TRADE</option><option value="ibkr">Interactive Brokers</option><option value="tastytrade">tastytrade</option><option value="public">Public</option><option value="sofi">SoFi Invest</option><option value="ally">Ally Invest</option><option value="tradestation">TradeStation</option><option value="firstrade">Firstrade</option><option value="moomoo">moomoo</option></select>
</div>
<div class="hint" style="margin-top:8px">Brokers don't allow outside websites to place trades for you (that needs their own app + your login). "Open in broker" copies the exact order to your clipboard and opens the ticker at your broker — paste and confirm there.</div>
</div>""")
    parts.append(f"""<h2>Performance</h2>
<div class="record">
<div class="stat"><div class="v">{record['wins']}-{record['losses']}</div><div class="l">Win / Loss</div></div>
<div class="stat"><div class="v" style="color:{'#34d399' if record['total_pl']>=0 else '#fb7185'}">{record['total_pl']:+.1f}%</div><div class="l">Est. cum P/L</div></div>
<div class="stat"><div class="v">{record['open']}</div><div class="l">Open</div></div>
</div>
<div class="hint">Since {e(record['since'])} · graded automatically after {C.GRADE_WINDOW_DAYS} trading days</div>
<div class="chart">{_spark(record['series'])}</div>
<div class="disc"><b>Not financial advice.</b> This is an automated research &amp; education experiment,
built for tracking a system — not professional trading guidance. Options can lose 100% of the premium paid.
Never trade money you can't afford to lose. The moon/numerology layer is for fun and weighted accordingly.</div>
<div class="foot">Generated by St0ckMarken · conviction threshold {C.MIN_CONVICTION:.0f} · free data via Yahoo Finance ·
flat 1-position sizing · for your own records</div>""")
    graded = [{"date": r["date"], "t": r["ticker"], "pl": float(r["est_pl_pct"] or 0), "result": r["result"]}
              for r in (picks_rows or []) if r.get("status") == "GRADED"]
    sm_data = {"plays": [{"t": p["ticker"], "date": date_str, "kind": p["kind"], "cost": p["cost"],
                           "prem": p["premium"], "spot": p["spot"]} for p in plays],
               "graded": graded}
    parts.append(f'</div><script>window.SM_DATA={json.dumps(sm_data)};</script>'
                 '<script src="budget.js"></script></body></html>')
    return "".join(parts)
