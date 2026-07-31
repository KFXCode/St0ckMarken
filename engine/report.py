"""Bright, fun, modern-futuristic mobile report — white theme, beginner-friendly."""
import html, json
from . import config as C

CSS = """
:root{--bg:#ffffff;--ink:#151530;--dim:#6b7280;--line:#e9ebf7;--soft:#f4f6ff;
--primary:#6c5ce7;--primary2:#3aa0ff;--green:#00b46e;--red:#ff4d6d;--sun:#ff9f1c;--violet:#7c5cff;--card:#ffffff}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
padding:0 0 50px;max-width:540px;margin:0 auto;-webkit-font-smoothing:antialiased}
.wrap{padding:16px}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;position:sticky;top:0;
background:rgba(255,255,255,.9);backdrop-filter:blur(10px);z-index:6;border-bottom:1px solid var(--line)}
.brand{font-size:20px;font-weight:900;letter-spacing:-.02em;background:linear-gradient(90deg,var(--primary),var(--primary2));
-webkit-background-clip:text;background-clip:text;color:transparent}
.hero{margin:16px;padding:22px 20px;border-radius:22px;color:#fff;
background:linear-gradient(135deg,#6c5ce7 0%,#7c5cff 45%,#3aa0ff 100%);box-shadow:0 12px 30px rgba(108,92,231,.28)}
.hero .pl{font-size:13px;opacity:.9} .hero .pv{font-size:40px;font-weight:900;letter-spacing:-.03em;margin-top:2px}
.hero .pc{font-size:15px;font-weight:700;margin-top:2px}
.hero .mkt{font-size:12.5px;opacity:.92;margin-top:10px;background:rgba(255,255,255,.16);border-radius:12px;padding:8px 12px}
a{color:var(--primary)} a:hover{color:var(--primary2)}
h2{font-size:19px;margin:26px 0 8px;font-weight:800;letter-spacing:-.01em}
.hint{color:var(--dim);font-size:13px}
.card{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:18px;margin:16px 0;
box-shadow:0 8px 24px rgba(90,90,160,.07)}
.playtag{font-size:11.5px;letter-spacing:.1em;color:var(--violet);text-transform:uppercase;font-weight:800}
.title{font-size:22px;font-weight:900;margin:5px 0 2px;letter-spacing:-.01em}
.sub{color:var(--dim);font-size:13.5px}
.dir-b{color:var(--green)} .dir-s{color:var(--red)}
.stats{display:flex;gap:9px;margin:14px 0}
.stat{flex:1;background:var(--soft);border-radius:14px;padding:11px 6px;text-align:center}
.stat .v{font-size:20px;font-weight:900} .stat .l{font-size:10.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em;font-weight:700}
.plain{background:#eafaf1;border:1px solid #bfead2;border-radius:14px;padding:12px 14px;font-size:14px;margin:12px 0;color:#0a6b45}
.plain.bear{background:#fff0f3;border-color:#ffc9d4;color:#a01f3c}
ul{margin:8px 0 0 18px;font-size:14px;color:#3b3b52} li{margin:4px 0}
.why{font-size:14px;font-weight:800;margin-top:14px}
.tagrow{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.tag{font-size:12px;padding:4px 11px;border-radius:99px;background:var(--soft);border:1px solid var(--line);color:var(--dim);font-weight:600}
.tag.good{color:#0a6b45;background:#e5faef;border-color:#bfead2}
.avoid{background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px 14px;margin:10px 0;font-size:14px}
.avoid b{font-size:15px}
.record{display:flex;gap:9px;margin:16px 0}
.chart{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:14px;margin:14px 0;box-shadow:0 8px 24px rgba(90,90,160,.07)}
.foot{color:var(--dim);font-size:12.5px;text-align:center;margin-top:28px;line-height:1.7}
.disc{background:linear-gradient(135deg,#fff4e6,#ffe9ee);border:1.5px solid #ffcf9e;border-radius:18px;
padding:16px 16px;margin:22px 0;font-size:13.5px;color:#8a4b12;line-height:1.6}
.disc b{color:#b3400f}
button{cursor:pointer;font-family:inherit}
.take{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:14px;border-top:1px solid var(--line);padding-top:14px}
.tbtn{width:36px;height:36px;border-radius:12px;background:var(--soft);border:1px solid var(--line);color:var(--ink);font-size:19px;font-weight:800}
.tq{min-width:24px;text-align:center;font-weight:900;font-size:17px}
.takebtn{background:linear-gradient(135deg,var(--green),#12c98a);border:none;color:#fff;border-radius:12px;padding:10px 16px;font-size:14px;font-weight:800;box-shadow:0 6px 16px rgba(0,180,110,.28)}
.takebtn:disabled{opacity:.5;cursor:default;box-shadow:none}
.pot{font-size:12.5px;color:var(--dim);width:100%}
.pos{background:var(--soft);border-radius:12px;padding:9px 11px;margin:6px 0;font-size:14px}
input,select{font-family:inherit}
#sm-amt,#sm-goal,.numin{flex:1;min-width:0;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:11px 13px;color:var(--ink);font-size:16px}
.linkbtn{background:none;border:none;color:var(--dim);font-size:12.5px;text-decoration:underline;margin-top:12px;padding:0}
.pillbtn{border:1.5px solid var(--line);background:#fff;color:var(--ink);border-radius:12px;padding:9px 12px;font-size:13.5px;font-weight:700}
.guide{background:linear-gradient(135deg,#f6f4ff,#eef6ff);border:1px solid #e2ddff;border-radius:20px;padding:4px 18px;margin:16px 0}
.guide summary{font-size:15.5px;font-weight:800;padding:14px 0;cursor:pointer;color:var(--primary)}
.gsec{font-size:14px;color:#3b3b52;margin:0 0 14px;line-height:1.62}
.gsec b{color:var(--ink)}
.flow{background:#e9fbf3;border:1px solid #c3edda;border-radius:16px;padding:13px 15px;margin:10px 0;font-size:14px;color:#0a6b45}
.flow b{color:#087a4e}
.buzz{background:#f4f0ff;border:1px solid #e0d8ff;border-radius:16px;padding:13px 15px;margin:10px 0;font-size:14px;color:#4a3a8c}
.buzz b{color:var(--violet)}
.pill{display:inline-block;font-size:12px;padding:4px 11px;border-radius:99px;background:#fff;border:1px solid var(--line);color:var(--ink);margin:4px 5px 0 0;font-weight:600}
.cndl{background:#eef4ff;border:1px solid #cfe0ff;border-radius:14px;padding:12px 14px;font-size:13.5px;margin:12px 0;color:#1f4d8a}
.cndl b{color:#144a9c}
.grok{background:#f2fae6;border:1px solid #d5eeb2;border-radius:14px;padding:12px 14px;font-size:13.5px;margin:12px 0;color:#3f5a15}
.grok b{color:#3f7a12}
.grow{background:#eafaf1;border:1px solid #bfead2;border-radius:14px;padding:12px 14px;font-size:13.5px;margin:12px 0;color:#0a6b45}
.grow b{color:#087a4e}
.hist{background:#faf0ff;border:1px solid #eacfff;border-radius:14px;padding:12px 14px;font-size:13.5px;margin:12px 0;color:#6a2a9e}
.hist b{color:#7a1fb0}
.brokerbtn{background:#fff;border:1.5px solid var(--primary);color:var(--primary);border-radius:12px;padding:10px 16px;font-size:14px;font-weight:800}
.scn{display:flex;justify-content:space-between;font-size:12.5px;color:var(--dim);padding:3px 0;border-bottom:1px dashed #e3e6f4}
.scn:last-child{border-bottom:none} .scn-h{color:var(--ink);font-weight:800}
.selrow{display:flex;gap:9px;align-items:center;margin-top:12px}
.sel{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:11px 12px;color:var(--ink);font-size:15px;font-weight:600;flex:1;min-width:0}
.filterbar{position:sticky;top:57px;z-index:5;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);
padding:10px 0;margin:0 0 4px}
.watch{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:15px;margin:12px 0;box-shadow:0 8px 24px rgba(90,90,160,.07)}
.wtop{display:flex;justify-content:space-between;align-items:baseline}
.wname{font-size:17px;font-weight:900} .wprice{font-size:15px;font-weight:800}
.meme{background:linear-gradient(135deg,#fff0f6,#fff6e6);border:1.5px solid #ffcfe0}
.trade summary{list-style:none;cursor:pointer;outline:none}
.trade summary::-webkit-details-marker{display:none}
.trade .chev{font-size:15px;color:var(--dim);transition:transform .2s}
.trade[open] .chev{transform:rotate(180deg)}
.modetabs{display:flex;gap:8px;background:var(--soft);border-radius:14px;padding:5px}
.modebtn{flex:1;border:none;background:transparent;color:var(--dim);border-radius:10px;padding:11px 8px;font-size:14.5px;font-weight:800}
.modebtn.active{background:#fff;color:var(--primary);box-shadow:0 3px 10px rgba(90,90,160,.14)}
"""

GUIDE = """
<details class="guide" open>
<summary>👋 How to use this app (read me first!)</summary>
<div class="gsec"><b>What this app is.</b> Every morning a robot looks at hundreds of stocks (and crypto, forex &amp; commodities) and picks a few really good ones it thinks will go up or down. It shows you exactly what to do. Your job is just to copy the trade. Easy!</div>
<div class="gsec"><b>Step 1 — set your money.</b> At the top in <b>My Money</b>, type how much you're starting with (even $20 is fine) and tap <b>Start</b>. It's pretend money so you can practice with zero risk. You can change it any time with the <b>Add</b>, <b>Take out</b>, or <b>New amount</b> buttons.</div>
<div class="gsec"><b>Step 2 — pick your market.</b> Use the <b>market dropdown</b> to choose Stocks, Crypto, Forex, Commodities, or Meme coins. Look for the green <b>$100-friendly ✓</b> tag — those are cheap enough for a small budget.</div>
<div class="gsec"><b>Step 3 — read the trade.</b> The <b>green box</b> says it in plain English, the <b>blue box</b> shows chart shapes the robot spotted, and <b>"How your money can grow"</b> shows what you could make… and the most you could lose (never more than you pay).</div>
<div class="gsec"><b>Step 4 — take the trade.</b> Pick how many with <b>−</b>/<b>+</b>, tap <b>Take this trade</b> to add it to your practice money. Ready for real? Pick your broker up top, then tap <b>Open in [your broker]</b> — it copies the order so you paste &amp; buy in your app.</div>
<div class="gsec"><b>⭐ Golden rules.</b> 1) Only use money you're okay losing. 2) Start with cheap trades. 3) Nothing sells by itself — you must tap <b>Sell to Close</b> in your broker to keep profit. 4) Slow and steady wins — small wins stack into big money over time.</div>
</details>
<details class="guide">
<summary>📗 New to options? The plain-English guide</summary>
<div class="gsec"><b>What you're buying.</b> A <b>call</b> is like a coupon: the right to buy 100 shares at a set price (the <b>strike</b>) until a set date (the <b>expiration</b>). A <b>put</b> is the same but it wins when the stock FALLS. The coupon's price is the <b>premium</b>: premium $0.82 = one contract costs $82 (×100). You never have to buy the shares — almost everyone just sells the coupon once it's worth more.</div>
<div class="gsec"><b>Turn on options first (one time).</b> In your broker: <i>Settings → Options → Enable</i> (Robinhood, Webull) or apply for options approval (Fidelity, Schwab). <b>Level 1–2 approval</b> is all you need to buy calls and puts.</div>
<div class="gsec"><b>⚠️ It does NOT sell itself.</b> If the premium rises, the profit is only yours when you tap <b>Sell to Close</b>. Every day an option loses a little value (<b>time decay</b>); at expiration an out-of-the-money option becomes worthless — you lose the premium. Sell it yourself before expiry week.</div>
<div class="gsec"><b>Simple exit plan.</b> Decide before you buy: take profit at +50% to +100%; cut losses at −50%; and be out at least a week before expiration.</div>
</details>"""

def _spark(series):
    if len(series) < 2:
        return '<div class="hint">Chart appears once at least two trades are graded.</div>'
    w, h = 560, 120
    lo, hi = min(series + [0]), max(series + [0])
    rng = (hi - lo) or 1
    pts = " ".join(f"{i*(w/(len(series)-1)):.1f},{h-(v-lo)/rng*h:.1f}" for i, v in enumerate(series))
    zero_y = h - (0 - lo) / rng * h
    color = "#00b46e" if series[-1] >= 0 else "#ff4d6d"
    return (f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto">'
            f'<line x1="0" y1="{zero_y:.1f}" x2="{w}" y2="{zero_y:.1f}" stroke="#e3e6f4" stroke-dasharray="4 4"/>'
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/></svg>')

BUDGET_CARD = """<h2>💰 My Money</h2>
<div class="card" id="sm-budget">
<div id="sm-setup">
<div class="title" style="font-size:18px">Set your starting money</div>
<div class="hint">Any amount — even $20 works. It's practice money and stays on your device.</div>
<div class="selrow">
<input id="sm-amt" type="number" min="1" inputmode="decimal" placeholder="e.g. 20">
<button class="takebtn" id="sm-start-btn">Start</button>
</div></div>
<div id="sm-dash" style="display:none">
<div class="stats">
<div class="stat"><div class="v" id="sm-v-start">$0</div><div class="l">Started</div></div>
<div class="stat"><div class="v" id="sm-v-now">$0</div><div class="l">Now</div></div>
<div class="stat"><div class="v" id="sm-v-gr">0%</div><div class="l">Growth</div></div>
</div>
<div class="hint" id="sm-cash"></div>
<div class="selrow" style="flex-wrap:wrap">
<button class="pillbtn" id="sm-add">＋ Add money</button>
<button class="pillbtn" id="sm-remove">－ Take out</button>
<button class="pillbtn" id="sm-change">✏️ New amount</button>
</div>
<div style="border-top:1px solid var(--line);margin-top:14px;padding-top:12px">
<div class="why" style="margin-top:0">🎯 My weekly goal</div>
<div class="selrow"><span class="hint" style="white-space:nowrap">Make per week:</span>
<input id="sm-goal" type="number" min="1" inputmode="decimal" placeholder="e.g. 100"></div>
<div id="sm-goal-out" style="margin-top:10px"><span class="hint">Type a weekly $ goal to see the honest math.</span></div>
</div>
<div id="sm-open"></div><div id="sm-closed"></div>
<div id="sm-weekly" style="border-top:1px solid var(--line);margin-top:14px;padding-top:12px"></div>
<button class="linkbtn" id="sm-reset">Reset everything</button>
</div>
<div class="selrow"><span class="hint" style="white-space:nowrap">🏦 Your broker:</span>
<select id="sm-broker" class="sel"><option value="robinhood">Robinhood</option><option value="webull">Webull</option><option value="fidelity">Fidelity</option><option value="schwab">Charles Schwab</option><option value="thinkorswim">thinkorswim</option><option value="etrade">E*TRADE</option><option value="ibkr">Interactive Brokers</option><option value="tastytrade">tastytrade</option><option value="public">Public</option><option value="sofi">SoFi Invest</option><option value="ally">Ally Invest</option><option value="tradestation">TradeStation</option><option value="firstrade">Firstrade</option><option value="moomoo">moomoo</option><option value="coinbase">Coinbase (crypto)</option></select>
</div>
<div class="hint" style="margin-top:8px">Brokers don't let outside websites place trades for you. <b>Open in [broker]</b> copies the exact order and opens the ticker in your broker — you just paste &amp; confirm.</div>
</div>
<h2>🔎 Choose your market</h2>
<div class="filterbar"><select id="sm-asset" class="sel" style="width:100%">
<option value="all">⭐ Show everything</option>
<option value="stocks">📈 Stocks &amp; options</option>
<option value="crypto">🪙 Crypto</option>
<option value="forex">💱 Forex</option>
<option value="commodities">🛢️ Commodities</option>
<option value="meme">🐕 Meme coins (high risk)</option>
</select></div>"""

def _watch_card(w, asset, meme=False):
    dircls = "dir-b" if w["direction"] == "BULLISH" else "dir-s"
    arrow = "▲" if w["chg"] >= 0 else "▼"
    chgcol = "var(--green)" if w["chg"] >= 0 else "var(--red)"
    lean = "leaning UP" if w["direction"] == "BULLISH" else "leaning DOWN"
    pat = f" Chart shape spotted: <b>{html.escape(w['pattern_name'])}</b> — {html.escape(w['pattern'])}" if w.get("pattern_name") else ""
    section = "Crypto" if asset == "crypto" else "Forex" if asset == "forex" else "Commodity" if asset == "commodities" else "Meme coin"
    warn = '<div class="hint" style="color:#b3400f;margin-top:8px">⚠️ Meme coins are a high-risk lottery — only ever use tiny money you\'re 100% fine losing.</div>' if meme else ''
    price = f"${w['price']:,.4f}" if w["price"] < 1 else f"${w['price']:,.2f}"
    base = w["symbol"].replace("-USD", "").replace("=X", "")
    if w.get("is_trade"):
        size = C.SPOT_POSITION_USD
        grow = (f'<div class="grow"><b>How this trade works:</b> buy about <b>${size} of {html.escape(w["name"])}</b> at {price} — '
                f'you own the real thing (spot), so there is no expiration and no time decay. If it rises 10%, your ${size} becomes '
                f'${size*1.1:.0f}; if it rises 50%, ${size*1.5:.0f}. Worst case it drops hard — you can lose most of what you put in, '
                f'so keep the size small.{" This is a meme coin: treat it as pure lottery money." if meme else ""}</div>')
        return f"""<div class="card{' meme' if meme else ''}" data-asset="{asset}">
<div class="playtag">Suggested {section} trade · spot buy</div>
<div class="wtop"><div class="title" style="margin:0">{html.escape(w['name'])} <span class="{dircls}">BUY</span></div><div class="wprice">{price}</div></div>
<div class="stats">
<div class="stat"><div class="v">{w['conv']:.0f}</div><div class="l">Conviction</div></div>
<div class="stat"><div class="v">{w['score']:.0f}</div><div class="l">Score /100</div></div>
<div class="stat"><div class="v" style="color:{chgcol}">{arrow} {w['chg']:+.1f}%</div><div class="l">This week</div></div>
</div>
<div class="plain"><b>In plain English:</b> the robot sees {html.escape(w['trend'])} — a good-looking {"momentum" if meme else "setup"}. Suggested size: about ${size}.</div>{grow}
<div class="cndl"><b>📊 Chart shape:</b>{pat if pat else " no strong pattern — riding the trend"}.{warn}</div>
<div class="hint">Trade this in your broker's <b>{section} section</b>. <a href="https://finance.yahoo.com/quote/{html.escape(w['symbol'])}" target="_blank">Live chart →</a></div>
<div class="take" data-t="{html.escape(w['symbol'])}" data-base="{html.escape(base)}" data-date="__DATE__" data-cost="{size}" data-prem="{w['price']}" data-spot="{w['price']}" data-kind="SPOT" data-strike="0" data-exp="" data-action="BUY">
<span class="hint">Practice size ${size}</span><button class="takebtn">Take this trade</button><button class="brokerbtn">Open in broker</button>
<div class="pot"></div></div>
</div>"""
    return f"""<div class="watch{' meme' if meme else ''}" data-asset="{asset}">
<div class="wtop"><div class="wname">{html.escape(w['name'])} <span class="{dircls}">{lean}</span></div>
<div class="wprice">{price}</div></div>
<div class="hint">{section} · <span style="color:{chgcol};font-weight:700">{arrow} {w['chg']:+.1f}% this week</span> · robot score {w['score']:.0f}/100 · <b>watch only</b> (signal not strong enough to suggest yet)</div>
<div class="cndl" style="margin-top:10px">The robot sees {html.escape(w['trend'])}.{pat}{warn}</div>
<div class="hint" style="margin-top:8px">💡 Trade this in your broker's <b>{section} section</b> (not as an option). <a href="https://finance.yahoo.com/quote/{html.escape(w['symbol'])}" target="_blank">See the live chart →</a></div>
</div>"""

def _stock_card(p, i, date_str):
    e = html.escape
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
    c2, c5 = p["cost"] * 2, p["cost"] * 5
    grow_html = (f'<div class="grow"><b>How your money can grow:</b> you pay ~${p["cost"]:,.0f} once (the ${p["premium"]:.2f} premium '
                 f'× 100 shares) — and that is your entire risk. The contract moves several times faster than the stock. '
                 f'If the premium doubles to ${p["premium"]*2:.2f}, your ${p["cost"]:,.0f} becomes ${c2:,.0f} (+100%). '
                 f'On a big move past the ${p["strike"]:.0f} strike it could reach ${p["premium"]*5:.2f}, turning ${p["cost"]:,.0f} into '
                 f'${c5:,.0f} (+400%). <b>Can you lose more than ${p["cost"]:,.0f}?</b> No — buying a call or put caps your loss at exactly what you paid. '
                 f'<b>Can you gain more?</b> Yes — the upside is uncapped. <b>Remember:</b> profits are NOT automatic — tap "Sell to Close" in your broker to lock them in.</div>')
    budget = '<span class="tag good">$100-friendly ✓</span>' if p["budget_ok"] else \
             f'<span class="tag">needs ~${p["cost"]:,.0f}</span>'
    return f"""<div class="card" data-asset="stocks" data-screen-label="Trade {i}">
<details class="trade"><summary>
<div class="playtag">Trade #{i} · {e(p.get('timeframe','SWING'))} · {e(p['size'])}</div>
<div class="title">{e(p['ticker'])} <span class="{dircls}">{e(p['kind'])}</span> <span class="chev">▾</span></div>
<div class="sub">{e(p['action'])} the ${p['strike']:.0f} strike · expires {e(p['expiry'])} · stock at ${p['spot']:.2f}</div>
<div class="stats">
<div class="stat"><div class="v">{p['conviction']:.0f}</div><div class="l">Conviction</div></div>
<div class="stat"><div class="v">{p['score']:.0f}</div><div class="l">Score /100</div></div>
<div class="stat"><div class="v">${p['premium']:.2f}</div><div class="l">Premium</div></div>
</div></summary>
<div class="plain{bearcls}"><b>In plain English:</b> {e(p['plain'])}</div>{grow_html}{cndl_html}{grok_html}{hist_html}
<div class="why">Why this trade sets up:</div><ul>{reasons}</ul>
<div class="tagrow">{budget}<span class="tag">OI {p['oi']:,}</span><span class="tag">{e(p['direction'].title())}</span></div>
</details>
<div class="take" data-t="{e(p['ticker'])}" data-date="{e(date_str)}" data-cost="{p['cost']}" data-prem="{p['premium']}" data-spot="{p['spot']}" data-kind="{e(p['kind'])}" data-strike="{p['strike']:.0f}" data-exp="{e(p['expiry'])}" data-action="{e(p['action'])}">
<button class="tbtn" data-d="-1">−</button><span class="tq">1</span><button class="tbtn" data-d="1">+</button>
<span class="hint">contracts</span><button class="takebtn">Take this trade</button><button class="brokerbtn">Open in broker</button>
<div class="pot"></div></div>
</div>"""

def render(date_str, updated_str, beginner, experienced, record, flavor_meta,
           market, earnings_warnings, warnings, picks_rows=None,
           congress_top=None, social_top=None, playbook=None, grok_on=False,
           watch=None, meme=None):
    e = html.escape
    parts = [f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#6c5ce7"><meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="St0ckMarken">
<title>St0ckMarken — {e(date_str)}</title><style>{CSS}</style></head><body>
<div class="topbar"><div class="brand">St0ckMarken ✨</div>
<div class="hint" style="text-align:right;line-height:1.3">Updated<br><span style="font-size:11px">{e(updated_str)}</span></div></div>
<div class="hero"><div class="pl">Your practice portfolio</div>
<div class="pv" id="sm-hero-pv">Set money ↓</div>
<div class="pc" id="sm-hero-pc"></div>
<div class="mkt">📊 SPY {market['spy']} ({market['spy_chg']:+.1f}%) · VIX {market['vix']} · {len(beginner or [])+len(experienced or [])} trades today · scanned {market['scanned']}</div></div>
<div class="wrap">"""]
    parts.append(BUDGET_CARD)
    parts.append(GUIDE)
    for wtxt in warnings:
        parts.append(f'<div class="disc"><b>Heads up:</b> {e(wtxt)}</div>')
    if earnings_warnings:
        items = "".join(f"<li>{e(x)}</li>" for x in earnings_warnings)
        parts.append(f'<div class="disc"><b>Earnings this week — extra risk</b><ul>{items}</ul></div>')
    parts.append('<h2>🎓 Choose your level</h2>'
                 '<div class="filterbar"><div class="modetabs">'
                 '<button class="modebtn" data-mode="beginner">🌱 Beginner</button>'
                 '<button class="modebtn" data-mode="experienced">🚀 Experienced</button>'
                 '</div></div>')
    plays = (beginner or []) + (experienced or [])
    # ---- Beginner stock trades (cheap / low-priced) ----
    parts.append('<div data-mode="beginner">')
    parts.append('<h2 data-asset="stocks">📈 Beginner Stock Option Trades <span class="hint" style="font-weight:600">(cheap, small-account)</span></h2>')
    if not beginner:
        parts.append('<div class="card" data-asset="stocks"><div class="title">No beginner trades today</div>'
                     f'<div class="hint">Nothing low-priced cleared the safety bar ({C.MIN_CONVICTION:.0f}+ conviction). No filler trades — staying in cash IS a smart move.</div></div>')
    for i, p in enumerate(beginner or [], 1):
        parts.append(_stock_card(p, i, date_str))
    parts.append('</div>')
    # ---- Experienced stock trades (higher-value, real trades) ----
    parts.append('<div data-mode="experienced" style="display:none">')
    parts.append('<h2 data-asset="stocks">🚀 Experienced Stock Option Trades <span class="hint" style="font-weight:600">(higher-value real trades)</span></h2>')
    parts.append('<div class="hint" data-asset="stocks">Best-conviction setups regardless of price — these can cost $100–$500+ per contract. Same full breakdown, bigger names.</div>')
    if not experienced:
        parts.append('<div class="card" data-asset="stocks"><div class="title">No experienced trades today</div>'
                     f'<div class="hint">Nothing cleared the safety bar ({C.MIN_CONVICTION:.0f}+ conviction) at higher price points today.</div></div>')
    for i, p in enumerate(experienced or [], 1):
        parts.append(_stock_card(p, i, date_str))
    parts.append('</div>')

    # ---- Other markets: crypto / forex / commodities ----
    labels = {"crypto": "🪙 Crypto Watch", "forex": "💱 Forex Watch", "commodities": "🛢️ Commodities Watch"}
    for cls in ("crypto", "forex", "commodities"):
        items = (watch or {}).get(cls) or []
        parts.append(f'<h2 data-asset="{cls}">{labels[cls]}</h2>')
        if items:
            parts.append(f'<div class="hint" data-asset="{cls}">Top movers our robot is watching. These trade as the real thing (spot), not options.</div>')
            for w in items:
                parts.append(_watch_card(w, cls))
        else:
            parts.append(f'<div class="watch" data-asset="{cls}"><div class="hint">⏳ {labels[cls].split(" ",1)[1] if " " in labels[cls] else cls} data didn\'t load from Yahoo this run (it sometimes rate-limits). It\'ll refresh on the next daily update.</div></div>')

    # ---- Meme coins ----
    parts.append('<h2 data-asset="meme">🐕 Meme Coin Watch <span style="font-size:13px;color:var(--red)">(high risk!)</span></h2>')
    parts.append('<div class="disc" data-asset="meme"><b>Real talk:</b> meme coins are NOT low-risk. They can go up huge or drop to almost nothing in a day. This is lottery-ticket money — only ever put in tiny amounts you are totally fine losing. There is no such thing as "low risk, high reward" here.</div>')
    if meme:
        for w in meme:
            parts.append(_watch_card(w, "meme", meme=True))
    else:
        parts.append('<div class="watch meme" data-asset="meme"><div class="hint">⏳ Meme-coin data didn\'t load from Yahoo this run (it sometimes rate-limits). It\'ll refresh on the next daily update.</div></div>')

    if congress_top:
        rows = "".join(
            f'<div class="pill">{e(t)} · {b} buys{("/"+str(s)+" sells") if s else ""}'
            + (f' · {e(names[0])}' if names else "") + '</div>'
            for t, b, s, names in congress_top)
        parts.append(f'<h2>🏛️ Elite Flows Watch</h2><div class="hint">What lawmakers have been buying recently '
                     f'(free House/Senate disclosures). A confirmation layer, not a trigger.</div>'
                     f'<div class="flow"><b>Recent lawmaker buys:</b><br>{rows}</div>')
    if social_top:
        rows = "".join(
            f'<div class="pill">{e(t)} · {m} mentions{" · trending" if tr else ""}</div>'
            for t, m, bl, be, tr in social_top)
        parts.append(f'<h2>💬 Social Buzz</h2><div class="hint">Loudest retail chatter on StockTwits / Reddit. '
                     f'Heavy hype is often a <i>fade</i> — we weight this small.</div><div class="buzz"><b>Most talked-about:</b><br>{rows}</div>')
    if playbook:
        items = "".join(f'<li><b>{e(tf)}:</b> {e(desc)}</li>' for tf, desc in playbook)
        parts.append(f'<div class="buzz"><b>Proven strategy playbook</b> '
                     f'<span class="hint">(vetted tactics from trading X/Reddit, folded in as education)</span>'
                     f'<ul>{items}</ul></div>')
    parts.append('<div class="hint" style="margin:10px 0">'
                 + ('𝕏 Grok live X/news read is <b style="color:var(--green)">ON</b> for today\'s trades.' if grok_on
                    else 'Grok live-X layer is off (add an XAI_API_KEY secret to enable). Using free news + StockTwits/Reddit.')
                 + '</div>')
    parts.append(f"""<h2>🏆 Performance</h2>
<div class="record">
<div class="stat"><div class="v">{record['wins']}-{record['losses']}</div><div class="l">Win / Loss</div></div>
<div class="stat"><div class="v" style="color:{'#00b46e' if record['total_pl']>=0 else '#ff4d6d'}">{record['total_pl']:+.1f}%</div><div class="l">Est. cum P/L</div></div>
<div class="stat"><div class="v">{record['open']}</div><div class="l">Open</div></div>
</div>
<div class="hint">Since {e(record['since'])} · graded automatically after {C.GRADE_WINDOW_DAYS} trading days</div>
<div class="chart">{_spark(record['series'])}</div>
<div class="disc"><b>⚠️ NOT financial advice.</b> I am not a professional trader and this is an automated
research &amp; education experiment — nothing here is a recommendation to buy or sell anything. Trading stocks,
options, crypto, forex and commodities involves real risk, and options and crypto can lose 100% of your money
fast. Past results and backtests never guarantee the future. The moon / zodiac / numerology layer is just for
fun. <b>Do your own research and move at your own risk.</b> Only ever trade money you can afford to lose.</div>
<div class="foot">Made by St0ckMarken ✨ · safety threshold {C.MIN_CONVICTION:.0f} · free data via Yahoo Finance ·
flat 1-position sizing · practice money only</div>""")
    graded = [{"date": r["date"], "t": r["ticker"], "pl": float(r["est_pl_pct"] or 0), "result": r["result"]}
              for r in (picks_rows or []) if r.get("status") == "GRADED"]
    spot_plays = []
    for cls_items in (watch or {}).values():
        spot_plays += [w for w in cls_items if w.get("is_trade")]
    spot_plays += [w for w in (meme or []) if w.get("is_trade")]
    sm_plays = [{"t": p["ticker"], "date": date_str, "kind": p["kind"], "cost": p["cost"],
                 "prem": p["premium"], "spot": p["spot"]} for p in plays]
    sm_plays += [{"t": w["symbol"], "date": date_str, "kind": "SPOT", "cost": C.SPOT_POSITION_USD,
                  "prem": w["price"], "spot": w["price"]} for w in spot_plays]
    sm_data = {"plays": sm_plays, "graded": graded}
    parts.append(f'</div><script>window.SM_DATA={json.dumps(sm_data)};</script>'
                 '<script src="budget.js"></script></body></html>')
    return "".join(parts).replace("__DATE__", date_str)
