# St0ckMarken — Daily Options Recommendation Engine

Automated daily research: scans ~100 liquid US tickers before market open, grades each
on transparent signals, and publishes a mobile-friendly report of the top options plays
(plus a "why NOT to trade" list) via GitHub Pages. Same structure as the MLB betting engine.

> **Not financial advice.** Research/education experiment only. Options can lose 100%
> of the premium paid. Never trade money you can't afford to lose.

## How it works (daily, automatic)

1. **8:45 AM ET weekdays**, GitHub Actions runs `run.py` (also runnable manually via the
   Actions tab → "Daily options report" → Run workflow).
2. Grades any open picks past their 10-trading-day window (win/loss + est. premium P/L %).
3. Downloads 1 year of daily prices for the universe via **yfinance** (free, keyless).
4. Scores every ticker 0–100 on weighted signals (see `engine/config.py` — every weight
   and threshold is there):
   - Trend (25) · MACD (15) · Volume spike (15) · Relative strength vs SPY (15)
   - RSI (10) · Volatility fit (10) · News sentiment (5) · Moon/zodiac/numerology **flavor (5)**
5. Conviction = |score − 50| × 2. Only candidates with **conviction ≥ 20** become plays —
   no filler picks; a no-play day is a valid output.
6. Builds a concrete contract per play from the live Yahoo options chain:
   - Bullish → **long call** ~3% OTM, 20–45 DTE
   - Bearish → **long put** ~3% OTM
   - Bullish + rich volatility → **cash-secured put** ~5% OTM (collateral required)
   - Liquidity gates: open interest ≥ 100, bid > 0, spread ≤ 25% of mid
   - Contracts costing ≤ $100 get a **"$100-friendly"** tag for small accounts
7. Logs every pick to `data/picks.csv`, updates the running record, renders `docs/index.html`.

Sizing is always flat **"1 unit"** — you decide what a unit is.

## One-time setup

1. Create a GitHub repo named `St0ckMarken` (same account as the MLB repo is fine —
   every repo gets its own Actions schedule and Pages site).
2. Push these files to it.
3. **Settings → Pages** → Source: *Deploy from a branch* → Branch: `main`, folder: `/docs`.
4. **Settings → Actions → General** → Workflow permissions → *Read and write permissions*.
5. Actions tab → run "Daily options report" once manually to generate the first report.
6. Your report lives at `https://<your-username>.github.io/St0ckMarken/`.

## Grading rules (in `engine/tracker.py`)

- **Long calls/puts:** WIN if the underlying moves ≥ 1.5% in the pick's direction within
  10 trading days. Est. premium P/L% ≈ move% × (spot/premium) × 0.40 delta proxy, floored at −100%.
- **Cash-secured puts:** WIN if the stock closes at/above the strike at window end
  (you keep the full premium).

## Budget tracker (in the report)

Each report has a **My Budget** section: enter a starting budget (e.g. $100), tap
"Take this trade" on any pick (choose how many contracts), and the tracker deducts the
cost, shows estimated profit-if-it-wins, and automatically credits back proceeds when
the pick is graded — so your simulated bankroll grows/shrinks over time. It's all
stored in your browser (localStorage), private to your device; "Reset" starts over.

## Tuning

Everything is in `engine/config.py`: universe, weights, conviction threshold, DTE window,
strike offsets, budget tag, grade window. Raise `MIN_CONVICTION` for fewer/stronger picks.

## Expanding later

- Forex/other markets: add a new universe + data module; the scoring/report layers are generic.
- The flavor layer (moon/zodiac/numerology) is 5% weight, clearly labeled in the report, and
  can be zeroed in `WEIGHTS`.
