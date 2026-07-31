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
.tookbox{display:flex;align-items:center;gap:8px;width:100%;margin-top:10px;padding:10px 12px;background:var(--soft);border:1.5px solid var(--line);border-radius:12px;font-size:14px;font-weight:700;cursor:pointer}
.tookbox input{width:20px;height:20px;accent-color:var(--green)}
.limitbox{background:#fff7e6;border:1.5px solid #ffd98a;border-radius:14px;padding:12px 14px;font-size:13.5px;margin:12px 0;color:#8a5a12}
.limitbox b{color:#b3730f}
.botcard{background:linear-gradient(135deg,#efeaff,#e6f3ff);border:2px solid #c9bcff;border-radius:20px;padding:18px;margin:16px 0;box-shadow:0 8px 24px rgba(108,92,231,.14)}
.switch{position:relative;display:inline-block;width:52px;height:30px}
.switch input{opacity:0;width:0;height:0}
.slider2{position:absolute;cursor:pointer;inset:0;background:#c9c9db;border-radius:99px;transition:.2s}
.slider2:before{content:"";position:absolute;height:24px;width:24px;left:3px;top:3px;background:#fff;border-radius:50%;transition:.2s}
.switch input:checked+.slider2{background:#6c5ce7}
.switch input:checked+.slider2:before{transform:translateX(22px)}
.botgoal{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px 14px;font-size:13.5px;margin:12px 0}
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
</details>
<details class="guide">
<summary>⏰ What time should I trade? (super important!)</summary>
<div class="gsec"><b>All times are Eastern Time (ET)</b> — that's the clock the stock market uses. If you're on the West Coast, that's 3 hours EARLIER for you (10 AM ET = 7 AM your time).</div>
<div class="gsec"><b>📈 Stocks & options — Monday to Friday only:</b><br>
• <b>Market opens 9:30 AM ET, closes 4:00 PM ET.</b><br>
• <b>6–9 AM ET:</b> the app updates at 6 AM. Read the picks, no rush — the market's still closed.<br>
• <b>Skip 9:30–9:45 AM.</b> The first 15 minutes are crazy jumpy and you often overpay.<br>
• <b>⭐ BEST time to buy: 9:45–10:30 AM ET.</b> Prices calm down and get fair. If you only trade once, <b>10:00 AM ET is the sweet spot</b> — set a phone alarm!<br>
• Right after you buy, set the <b>sell-limit</b> the app gives you. Then you're done for the day.</div>
<div class="gsec"><b>🪙 Crypto — any time, 7 days a week.</b> It never closes! But calm times (mornings) are usually smoother than late nights.</div>
<div class="gsec"><b>💱 Forex — almost all week.</b> Opens Sunday evening, runs to Friday evening ET. Closed most of the weekend.</div>
<div class="gsec"><b>📢 One rule:</b> if the app shows an earnings warning for a stock that day, either skip it or expect a BIG swing either way.</div>
</details>
<details class="guide">
<summary>📖 Kid Dictionary — every trading word in easy words</summary>
<div class="gsec"><b>Call option</b> = A bet that a stock will go UP. Like saying "I think this toy will cost more later!"</div>
<div class="gsec"><b>Put option</b> = A bet that a stock will go DOWN.</div>
<div class="gsec"><b>Premium</b> = The price you paid for the bet. If it says $0.35, one bet costs $35 (you always times by 100).</div>
<div class="gsec"><b>Contract</b> = One full bet. One contract watches 100 shares of the stock.</div>
<div class="gsec"><b>Strike price</b> = The special number the stock has to pass for your bet to win.</div>
<div class="gsec"><b>Expiration (Expiry)</b> = The day your bet ends. After this day the bet is over.</div>
<div class="gsec"><b>Sell limit</b> = You tell the computer "Sell my bet when it reaches THIS price." Then you don't have to watch it — the computer does it for you.</div>
<div class="gsec"><b>Market order</b> = "Sell it right now!" at whatever price people are paying.</div>
<div class="gsec"><b>Bid</b> = The most someone will pay you right now. <b>Ask</b> = The least someone will sell to you for right now.</div>
<div class="gsec"><b>Expected swing (move)</b> = How much the computer thinks the price might jump. Like guessing how far a rubber band will stretch.</div>
<div class="gsec"><b>Profit</b> = The extra money you make. <b>Gain %</b> = How much bigger your money got. +50% means it grew by half!</div>
<div class="gsec"><b>Break-even</b> = The price where you don't win OR lose. You just get your money back.</div>
<div class="gsec"><b>Out of the money (OTM)</b> = Your bet isn't winning YET. <b>In the money (ITM)</b> = Your bet IS winning right now!</div>
<div class="gsec"><b>Leverage</b> = Your bet can grow way faster than the stock. Like a tiny push that moves a big swing.</div>
<div class="gsec"><b>Volatility (IV)</b> = How wild and jumpy a stock is. Jumpy = more exciting but more risky.</div>
<div class="gsec"><b>Max loss</b> = The MOST you can lose. Good news: it's only the money you paid — never more. 🛡️</div>
<div class="gsec"><b>Conviction</b> = How SURE the computer is about the bet. Higher number = more sure!</div>
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

BOT_CARD = """<h2>🤖 Auto-Bot (pretend money)</h2>
<div class="botcard">
<div class="hint" style="margin-bottom:10px">Turn this ON and the robot will <b>automatically "buy" trades for you every day</b> — no finger lifting! Its mission: <b>try to DOUBLE your money each day</b> by swinging big on the best picks (one trade, or a few trades — whatever it takes). It sets sell targets, closes bets, and keeps score. All <b>pretend money</b>, so you can watch a go-for-it bot with zero real risk.</div>
<div id="bot-setup">
<div class="title" style="font-size:18px">Give the bot some pretend money</div>
<div class="hint">Pick a start amount. The bot does the rest by itself.</div>
<div class="selrow">
<input id="bot-amt" type="number" min="1" inputmode="decimal" placeholder="e.g. 100" class="numin">
<button class="takebtn" id="bot-start-btn">Start the bot 🤖</button>
</div></div>
<div id="bot-dash" style="display:none">
<div class="selrow" style="justify-content:space-between;align-items:center;margin-top:0">
<span style="font-weight:800">Bot is running</span>
<label class="switch"><input type="checkbox" id="bot-toggle"><span class="slider2"></span></label>
</div>
<div class="stats" style="margin-top:12px">
<div class="stat"><div class="v" id="bot-v-start">$0</div><div class="l">Started</div></div>
<div class="stat"><div class="v" id="bot-v-now">$0</div><div class="l">Now</div></div>
<div class="stat"><div class="v" id="bot-v-gr">0%</div><div class="l">Growth</div></div>
</div>
<div class="hint" id="bot-record" style="margin:4px 0 10px"></div>
<div class="botgoal" id="bot-goal"></div>
<div class="selrow"><span class="hint" style="white-space:nowrap">Try to double in:</span>
<select id="bot-speed" class="sel">
<option value="7">About a week (safer 🐢)</option>
<option value="3">About 3 days (medium)</option>
<option value="1">About 1 day (wild 🔥)</option>
</select></div>
<div id="bot-list" style="margin-top:10px"></div>
<button class="linkbtn" id="bot-reset">Reset the bot</button>
</div>
<div class="hint" style="margin-top:8px">✅ <b>Robinhood-only:</b> the bot only takes trades you can actually make on Robinhood, so you can copy it. (It skips forex and gold/oil, which Robinhood doesn't do.)</div>
<div class="hint" style="margin-top:8px">🔒 <b>Real talk:</b> doubling money fast is a giant goal — no real bot or trader can promise it, and trying with real money is how people lose everything. That's why this bot uses <b>pretend money</b>: watch the wins AND the misses safely. A steady weekly double is already amazing if it keeps happening.</div>
</div>"""

BUDGET_CARD = """<h2>💰 My Pretend Money</h2>
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
    lean = "looks like it wants to go UP" if w["direction"] == "BULLISH" else "looks like it wants to go DOWN"
    pat = f" Shape the robot saw: <b>{html.escape(w['pattern_name'])}</b> — {html.escape(w['pattern'])}" if w.get("pattern_name") else ""
    section = "Crypto" if asset == "crypto" else "Forex" if asset == "forex" else "Commodity" if asset == "commodities" else "Meme coin"
    warn = '<div class="hint" style="color:#b3400f;margin-top:8px">⚠️ Meme coins are like a lottery ticket — they can jump up big OR drop to almost nothing fast. Only ever use tiny money you are totally okay losing.</div>' if meme else ''
    price = f"${w['price']:,.4f}" if w["price"] < 1 else f"${w['price']:,.2f}"
    base = w["symbol"].replace("-USD", "").replace("=X", "")
    RH_CRYPTO = {"BTC", "ETH", "SOL", "XRP", "ADA", "LINK", "AVAX", "LTC", "DOGE", "SHIB", "PEPE", "BONK"}
    if asset == "crypto":
        where = ("Robinhood has it ✓" if base in RH_CRYPTO else "not on Robinhood — use Coinbase or Kraken")
        where = f"📱 <b>Where to buy it:</b> {where} (you buy the real coin, not a bet)."
    elif asset == "meme":
        where = ("Robinhood has it ✓" if base in RH_CRYPTO else "usually NOT on Robinhood — use Coinbase")
        where = f"📱 <b>Where to buy it:</b> {where}. Only tiny money here!"
    elif asset == "forex":
        where = "📱 <b>Where to buy it:</b> Robinhood does NOT do this one — use OANDA, Interactive Brokers, or tastytrade."
    else:  # commodities
        where = "📱 <b>Where to buy it:</b> Robinhood does NOT do this one — use tastytrade or Interactive Brokers (or a look-alike stock like GLD or USO on Robinhood)."
    if w.get("is_trade"):
        size = C.SPOT_POSITION_USD
        grow = (f'<div class="grow"><b>How this works:</b> buy about <b>${size} of {html.escape(w["name"])}</b> at {price}. '
                f'You own the real thing, so there is no ending day — you can hold it as long as you want. If it goes up 10%, your ${size} turns into '
                f'about ${size*1.1:.0f}; if it goes up 50%, about ${size*1.5:.0f}. If it drops a lot you can lose most of your money, '
                f'so keep it small.{" This one is a meme coin — treat it like lottery money." if meme else ""}</div>')
        return f"""<div class="card{' meme' if meme else ''}" data-asset="{asset}">
<div class="playtag">Robot’s {section} pick · buy the real thing</div>
<div class="wtop"><div class="title" style="margin:0">{html.escape(w['name'])} <span class="{dircls}">BUY</span></div><div class="wprice">{price}</div></div>
<div class="stats">
<div class="stat"><div class="v">{w['conv']:.0f}</div><div class="l">How sure</div></div>
<div class="stat"><div class="v">{w['score']:.0f}</div><div class="l">Score /100</div></div>
<div class="stat"><div class="v" style="color:{chgcol}">{arrow} {w['chg']:+.1f}%</div><div class="l">This week</div></div>
</div>
<div class="plain"><b>What to do, in easy words:</b> the robot sees {html.escape(w['trend'])} — that looks good. Buy about ${size} of it.</div>{grow}
<div class="limitbox"><b>🎯 Best price to sell at: {("$%.4f" % (w['price']*(1+ (0.15 if meme else 0.10)))) if w['price']<1 else ("$%,.2f" % (w['price']*(1+ (0.15 if meme else 0.10))))}</b> (about +{15 if meme else 10}% bigger) · <b>📈 The robot thinks it could grow about +{15 if meme else 10}%</b>. Tell your app to sell when it reaches that price (a sell limit) — then it sells for you and you don’t have to watch!</div>
<div class="cndl"><b>📊 Shape the robot saw:</b>{pat if pat else " no clear shape — just following the trend"}.{warn}</div>
<div class="hint">{where} <a href="https://finance.yahoo.com/quote/{html.escape(w['symbol'])}" target="_blank">See the live chart →</a></div>
<div class="take" data-t="{html.escape(w['symbol'])}" data-base="{html.escape(base)}" data-date="__DATE__" data-cost="{size}" data-prem="{w['price']}" data-spot="{w['price']}" data-kind="SPOT" data-strike="0" data-exp="" data-action="BUY">
<span class="hint">Pretend size ${size}</span><button class="takebtn">Take this trade</button><button class="brokerbtn">Open in broker</button>
<div class="pot"></div></div>
</div>"""
    return f"""<div class="watch{' meme' if meme else ''}" data-asset="{asset}">
<div class="wtop"><div class="wname">{html.escape(w['name'])} <span class="{dircls}">{lean}</span></div>
<div class="wprice">{price}</div></div>
<div class="hint">{section} · <span style="color:{chgcol};font-weight:700">{arrow} {w['chg']:+.1f}% this week</span> · robot score {w['score']:.0f}/100 · <b>just watching</b> (not strong enough to buy yet)</div>
<div class="cndl" style="margin-top:10px">The robot sees {html.escape(w['trend'])}.{pat}{warn}</div>
<div class="hint" style="margin-top:8px">{where} <a href="https://finance.yahoo.com/quote/{html.escape(w['symbol'])}" target="_blank">See the live chart →</a></div>
</div>"""

def _stock_card(p, i, date_str):
    e = html.escape
    dircls = "dir-b" if p["direction"] == "BULLISH" else "dir-s"
    bearcls = "" if p["direction"] == "BULLISH" else " bear"
    reasons = "".join(f"<li><b>{e(k)}:</b> {e(n)}</li>" for k, n, _ in p["reasons"])
    pats = p.get("patterns") or []
    if pats:
        lis = "".join(f'<li><b>{e(nm)}</b> ({"looks like it wants to go UP" if d=="bull" else "looks like it wants to go DOWN"}): {e(pl)}</li>' for nm, d, pl in pats)
        cndl_html = f'<div class="cndl"><b>📊 Shapes the robot saw on the price chart:</b><ul>{lis}</ul></div>'
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
        sea = f" In past years, {h['month']} was usually {'a good' if h['sea']>=0 else 'a tricky'} month for {e(p['ticker'])} (about {h['sea']:+.1f}%)." if h.get("sea") is not None else ""
        hist_html = (f'<div class="hist"><b>What happened before (looking back {h["years"]:g} years):</b> this same setup showed up '
                     f'<b>{h["n"]}</b> times. When it did, the stock moved the way we hoped '
                     f'<b>{h["hit"]:.0f} out of every 100 times</b> (about {h["avg"]:+.1f}% at its best).{sea}</div>')
    else:
        hist_html = '<div class="hist"><b>What happened before:</b> we don\'t have many past examples of this exact setup, so be extra careful.</div>'
    c2, c5 = p["cost"] * 2, p["cost"] * 5
    grow_html = (f'<div class="grow"><b>How your money can grow:</b> you pay about <b>${p["cost"]:,.0f}</b> one time. That is the MOST you can lose — never more. '
                 f'A bet like this grows way faster than the stock (that is called leverage — a tiny push moves a big swing). '
                 f'If the bet\'s price doubles, your ${p["cost"]:,.0f} turns into <b>${c2:,.0f}</b> (that is +100%, your money got twice as big). '
                 f'On a really good move it could reach <b>${c5:,.0f}</b> (+400%, five times your money!). '
                 f'<b>Can you lose more than ${p["cost"]:,.0f}?</b> Nope — only what you paid. '
                 f'<b>Can you win more?</b> Yes — the top is wide open. '
                 f'<b>Remember:</b> the money is not yours until you SELL. Tap “Sell to Close” in your app to keep it.</div>')
    budget = '<span class="tag good">Great for $100 or less ✓</span>' if p["budget_ok"] else \
             f'<span class="tag">costs about ${p["cost"]:,.0f}</span>'
    rh = '<span class="tag good">✓ Works on Robinhood</span>'
    tp = min(1.2, 0.45 + max(0, p["conviction"] - 20) * 0.02)  # higher conviction → higher target
    sell_prem = p["premium"] * (1 + tp)
    profit = (sell_prem - p["premium"]) * 100
    und = abs(h["avg"]) if h and h.get("avg") is not None else max(4.0, p["conviction"] / 4)
    prem_swing = und * (0.45 * p["spot"] / p["premium"])  # premium %-swing per expected underlying move
    prem_swing = min(300, prem_swing)
    limit_html = (f'<div class="limitbox"><b>🎯 Best price to sell at: ${sell_prem:.2f}</b> '
                  f'(that is about +{tp*100:.0f}% bigger than what you paid) · <b>📈 The robot thinks it could grow about +{prem_swing:.0f}%</b> before the bet ends '
                  f'(because it thinks {e(p["ticker"])} will move about {und:.1f}%). '
                  f'Right after you buy, tell your app to “Sell when it reaches ${sell_prem:.2f}” (this is called a sell limit). '
                  f'Then the app sells it for you and you make about '
                  f'<b>+${profit:.0f} on each bet</b> — you don\'t even have to watch! Easy money.</div>')
    return f"""<div class="card" data-asset="stocks" data-screen-label="Trade {i}">
<details class="trade"><summary>
<div class="playtag">Trade #{i} · {e(p.get('timeframe','SWING'))} · {e(p['size'])}</div>
<div class="title">{e(p['ticker'])} <span class="{dircls}">{e(p['kind'])}</span> <span class="chev">▾</span></div>
<div class="sub">{e(p['action'])} the ${p['strike']:.0f} strike · expires {e(p['expiry'])} · stock at ${p['spot']:.2f}</div>
<div class="stats">
<div class="stat"><div class="v">{p['conviction']:.0f}</div><div class="l">How sure</div></div>
<div class="stat"><div class="v">{p['score']:.0f}</div><div class="l">Score /100</div></div>
<div class="stat"><div class="v">${p['premium']:.2f}</div><div class="l">Bet price</div></div>
</div></summary>
<div class="plain{bearcls}"><b>What to do, in easy words:</b> {e(p['plain'])}</div>{grow_html}{limit_html}{cndl_html}{grok_html}{hist_html}
<div class="why">Why the robot likes this bet:</div><ul>{reasons}</ul>
<div class="hint" style="margin-top:10px">📱 <b>Where to buy it:</b> this is a normal stock bet — you can buy it on <b>Robinhood</b> (tap the Options tab) or any big app (Webull, Fidelity, Schwab, tastytrade). If Robinhood doesn't show it, use tastytrade or Webull.</div>
<div class="tagrow">{budget}<span class="tag">OI {p['oi']:,}</span>{rh}</div>
</details>
<div class="take" data-t="{e(p['ticker'])}" data-date="{e(date_str)}" data-cost="{p['cost']}" data-prem="{p['premium']}" data-spot="{p['spot']}" data-kind="{e(p['kind'])}" data-strike="{p['strike']:.0f}" data-exp="{e(p['expiry'])}" data-action="{e(p['action'])}">
<button class="tbtn" data-d="-1">−</button><span class="tq">1</span><button class="tbtn" data-d="1">+</button>
<span class="hint">bets</span><button class="takebtn">Take this trade</button><button class="brokerbtn">Open in broker</button>
<div class="pot"></div></div>
</div>"""

def render(date_str, updated_str, beginner, experienced, record, flavor_meta,
           market, earnings_warnings, warnings, picks_rows=None,
           congress_top=None, social_top=None, playbook=None, grok_on=False,
           watch=None, meme=None, is_weekend=False):
    e = html.escape
    parts = [f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#6c5ce7"><meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="St0ckMarken">
<title>St0ckMarken — {e(date_str)}</title><style>{CSS}</style></head><body>
<div class="topbar"><div class="brand">St0ckMarken ✨</div>
<div class="hint" style="text-align:right;line-height:1.3">Updated<br><span style="font-size:11px">{e(updated_str)}</span></div></div>
<div class="hero"><div class="pl">Your pretend money</div>
<div class="pv" id="sm-hero-pv">Add money ↓</div>
<div class="pc" id="sm-hero-pc"></div>
<div class="mkt">📊 The whole market (SPY) is at {market['spy']} ({market['spy_chg']:+.1f}% today) · {len(beginner or [])+len(experienced or [])} good bets today · robot looked at {market['scanned']} stocks</div></div>
<div class="wrap">"""]
    parts.append(BUDGET_CARD)
    parts.append(BOT_CARD)
    parts.append(GUIDE)
    for wtxt in warnings:
        parts.append(f'<div class="disc"><b>Heads up:</b> {e(wtxt)}</div>')
    if earnings_warnings:
        items = "".join(f"<li>{e(x)}</li>" for x in earnings_warnings)
        parts.append(f'<div class="disc"><b>📢 Big news coming this week!</b> These companies share how much money they made soon, which can make the price jump a LOT either way — so be extra careful:<ul>{items}</ul></div>')
    parts.append('<h2>🎓 Pick how much money you have</h2>'
                 '<div class="filterbar"><div class="modetabs">'
                 '<button class="modebtn active" data-mode="beginner" onclick="smMode(\'beginner\')">🌱 Just starting</button>'
                 '<button class="modebtn" data-mode="experienced" onclick="smMode(\'experienced\')">🚀 More money</button>'
                 '</div></div>'
                 '<script>function smMode(m){document.querySelectorAll("[data-mode]:not(.modebtn)").forEach(function(el){el.style.display=el.dataset.mode===m?"":"none"});'
                 'document.querySelectorAll(".modebtn").forEach(function(b){b.classList.toggle("active",b.dataset.mode===m)});try{localStorage.setItem("sm_mode",JSON.stringify(m))}catch(e){}}'
                 'try{var _m=JSON.parse(localStorage.getItem("sm_mode")||"\\"beginner\\"");smMode(_m)}catch(e){}</script>')
    plays = (beginner or []) + (experienced or [])
    # ---- Beginner stock trades (cheap / low-priced) ----
    parts.append('<div data-mode="beginner">')
    if is_weekend:
        parts.append('<div class="disc" data-asset="stocks" style="background:linear-gradient(135deg,#e6f3ff,#efeaff);border-color:#c9bcff;color:#3a3a6a">'
                     '<b>😴 The stock market is closed on weekends.</b> Stocks and options only trade Monday–Friday. '
                     'New stock bets come back Monday morning! But good news — <b>🪙 crypto never sleeps and 💱 forex trades almost all week</b>, so scroll down for what\'s moving right now.</div>')
    parts.append('<h2 data-asset="stocks">📈 Cheap Bets for Small Money <span class="hint" style="font-weight:600">(great if you have $100 or less)</span></h2>')
    if not beginner:
        parts.append('<div class="card" data-asset="stocks"><div class="title">No cheap bets today</div>'
                     '<div class="hint">Nothing cheap looked good enough today. That is okay — keeping your money and NOT betting is a smart, safe move too!</div></div>')
    for i, p in enumerate(beginner or [], 1):
        parts.append(_stock_card(p, i, date_str))
    parts.append('</div>')
    # ---- Experienced stock trades (higher-value, real trades) ----
    parts.append('<div data-mode="experienced" style="display:none">')
    parts.append('<h2 data-asset="stocks">🚀 Bigger Bets for More Money <span class="hint" style="font-weight:600">(these cost more)</span></h2>')
    parts.append('<div class="hint" data-asset="stocks">The robot\'s most-sure bets, even the pricey ones — these can cost $100 to $500+ each. Same easy breakdown, just bigger name-brand stocks.</div>')
    if not experienced:
        parts.append('<div class="card" data-asset="stocks"><div class="title">No bigger bets today</div>'
                     '<div class="hint">Nothing pricey looked good enough today. Better to wait than to make a bad bet!</div></div>')
    for i, p in enumerate(experienced or [], 1):
        parts.append(_stock_card(p, i, date_str))
    parts.append('</div>')

    # ---- Other markets: crypto / forex / commodities ----
    labels = {"crypto": "🪙 Crypto (digital money)", "forex": "💱 Forex (money from other countries)", "commodities": "🛢️ Commodities (stuff like gold & oil)"}
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
    parts.append('<h2 data-asset="meme">🐕 Meme Coins <span style="font-size:13px;color:var(--red)">(super risky!)</span></h2>')
    parts.append('<div class="disc" data-asset="meme"><b>Be careful:</b> meme coins are like a lottery ticket. They can jump up really big OR drop to almost nothing in one day. Only ever use tiny money you are totally okay to lose. There is no “safe” bet here!</div>')
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
        parts.append(f'<h2>🏛️ What Important People Are Buying</h2><div class="hint">Some grown-ups who help run the country tell everyone what stocks they buy. '
                     f'The robot peeks at this as a little extra clue — not the main reason to bet.</div>'
                     f'<div class="flow"><b>Stuff they bought lately:</b><br>{rows}</div>')
    if social_top:
        rows = "".join(
            f'<div class="pill">{e(t)} · {m} mentions{" · trending" if tr else ""}</div>'
            for t, m, bl, be, tr in social_top)
        parts.append(f'<h2>💬 What Everyone Is Talking About</h2><div class="hint">The stocks people chat about most online. '
                     f'When EVERYONE is super excited, it can mean the opposite — so the robot only uses this a tiny bit.</div><div class="buzz"><b>Most talked-about:</b><br>{rows}</div>')
    if playbook:
        items = "".join(f'<li><b>{e(tf)}:</b> {e(desc)}</li>' for tf, desc in playbook)
        parts.append(f'<div class="buzz"><b>Smart trading tricks</b> '
                     f'<span class="hint">(good tips from real traders, put in easy words to learn from)</span>'
                     f'<ul>{items}</ul></div>')
    parts.append('<div class="hint" style="margin:10px 0">'
                 + ('𝕏 Grok live X/news read is <b style="color:var(--green)">ON</b> for today\'s trades.' if grok_on
                    else 'Grok live-X layer is off (add an XAI_API_KEY secret to enable). Using free news + StockTwits/Reddit.')
                 + '</div>')
    # ---- History: prior days' trades ----
    if picks_rows:
        by_date = {}
        for r in picks_rows:
            if r["date"] == date_str:
                continue
            by_date.setdefault(r["date"], []).append(r)
        if by_date:
            parts.append('<h2>📜 Old Bets — Did They Win?</h2><div class="hint">All the bets from earlier days and how they turned out. The robot checks each one after about 2 weeks.</div>')
            for d in sorted(by_date, reverse=True)[:14]:
                rows = ""
                for r in by_date[d]:
                    if r["status"] == "GRADED":
                        pl = r["est_pl_pct"]
                        col = "var(--green)" if str(pl).lstrip("-").replace(".", "").isdigit() and float(pl) >= 0 else "var(--red)"
                        res = f'<span style="color:{col};font-weight:700">{"WON 🎉" if r["result"]=="WIN" else "lost"} ({float(pl):+.0f}%)</span>'
                    else:
                        res = '<span class="hint">still going</span>'
                    kind = e(r["kind"])
                    tail = f' ${float(r["strike"]):.0f}' if r["kind"] != "SPOT" and r.get("strike") not in ("", "0", 0) else ""
                    rows += f'<div class="scn"><span>{e(r["ticker"])} · {kind}{tail}</span>{res}</div>'
                parts.append(f'<div class="card"><div class="playtag">{e(d)}</div>{rows}</div>')
    parts.append(f"""<h2>🏆 How We’re Doing</h2>
<div class="record">
<div class="stat"><div class="v">{record['wins']}-{record['losses']}</div><div class="l">Wins / Losses</div></div>
<div class="stat"><div class="v" style="color:{'#00b46e' if record['total_pl']>=0 else '#ff4d6d'}">{record['total_pl']:+.1f}%</div><div class="l">Money grown</div></div>
<div class="stat"><div class="v">{record['open']}</div><div class="l">Still going</div></div>
</div>
<div class="hint">Since {e(record['since'])} · the robot checks each bet after about 2 weeks</div>
<div class="chart">{_spark(record['series'])}</div>
<div class="disc"><b>⚠️ This is NOT real money advice.</b> This app is a fun way to LEARN about trading — it is not a grown-up telling you to buy or sell anything. '
Trading real money is risky, and bets can lose ALL the money you put in. What happened before does not promise what happens next. The moon and number stuff is just for fun. '
<b>Always ask a grown-up, and only ever use money you are okay to lose.</b></div>
<div class="foot">Made by St0ckMarken ✨ · a place to learn · free info from Yahoo Finance · pretend money only</div>""")
    graded = [{"date": r["date"], "t": r["ticker"], "pl": float(r["est_pl_pct"] or 0), "result": r["result"]}
              for r in (picks_rows or []) if r.get("status") == "GRADED"]
    spot_plays = []
    for cls_items in (watch or {}).values():
        spot_plays += [w for w in cls_items if w.get("is_trade")]
    spot_plays += [w for w in (meme or []) if w.get("is_trade")]
    RH_CRYPTO = {"BTC", "ETH", "SOL", "XRP", "ADA", "LINK", "AVAX", "LTC", "DOGE", "SHIB", "PEPE", "BONK"}
    sm_plays = [{"t": p["ticker"], "date": date_str, "kind": p["kind"], "cost": p["cost"],
                 "prem": p["premium"], "spot": p["spot"], "rh": True} for p in plays]  # stock options: all RH-tradeable
    sm_plays += [{"t": w["symbol"], "date": date_str, "kind": "SPOT", "cost": C.SPOT_POSITION_USD,
                  "prem": w["price"], "spot": w["price"],
                  "rh": w["symbol"].replace("-USD", "").replace("=X", "").replace("=F", "") in RH_CRYPTO}
                 for w in spot_plays]
    sm_data = {"plays": sm_plays, "graded": graded}
    parts.append(f'</div><script>window.SM_DATA={json.dumps(sm_data)};</script>'
                 '<script src="budget.js"></script></body></html>')
    return "".join(parts).replace("__DATE__", date_str)
