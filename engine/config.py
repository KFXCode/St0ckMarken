"""Central settings for the St0ckMarken options engine.
Every weight and threshold the strategy uses lives here — full transparency."""

# ---- Universe -------------------------------------------------------------
# ~100 liquid, optionable US names across the sectors you picked.
UNIVERSE = [
    # Tech / mega-caps
    "AAPL","MSFT","GOOGL","AMZN","META","NFLX","CRM","ORCL","ADBE","NOW",
    "SHOP","UBER","ABNB","PYPL","SQ","SNOW","PANW","CRWD","ZS","DDOG",
    # AI & semiconductors
    "NVDA","AMD","AVGO","TSM","INTC","MU","QCOM","ARM","SMCI","MRVL",
    "ASML","LRCX","AMAT","KLAC","ON","PLTR",
    # Energy
    "XOM","CVX","COP","OXY","SLB","HAL","DVN","FANG","MPC","VLO",
    # Financials
    "JPM","BAC","WFC","GS","MS","C","SCHW","COIN","HOOD","SOFI","V","MA","AXP",
    # Healthcare / biotech
    "UNH","JNJ","PFE","LLY","MRK","ABBV","MRNA","GILD","AMGN","VRTX","HIMS",
    # Meme / high-volatility
    "TSLA","GME","RIVN","NIO","MARA","RIOT","CLSK","DKNG",
    "RBLX","AFRM","UPST","CVNA","IONQ","RKLB","ASTS",
    # Low-priced / small-account favorites (optionable on Robinhood, cheap premiums)
    "PLUG","CHPT","GRAB","NU","PATH","LAZR",
    "SIRI","VALE","T","PBR","KGC","JBLU","SNAP","PARA","WBD",
    # Broad-market / consumer / industrial liquidity
    "SPY","QQQ","IWM","DIS","NKE","SBUX","MCD","WMT","COST","TGT",
    "HD","LOW","BA","CAT","DE","F","GM","AAL","DAL","CCL",
]

# ---- Signal weights (must sum to 100) --------------------------------------
WEIGHTS = {
    "trend":      20,   # SMA20/SMA50 alignment, price vs trend, 1-month return
    "candles":    12,   # Candlestick Trading Bible pattern recognition
    "macd":       10,   # MACD line vs signal + histogram slope
    "volume":     10,   # today's volume vs 20-day average
    "rel_str":    12,   # 1-month return vs SPY
    "rsi":         8,   # RSI(14) positioning
    "volatility":  8,   # historical-volatility percentile fit
    "sentiment":   5,   # free news-headline keyword sentiment
    "congress":    7,   # lawmaker/insider recent buys vs sells (elite flows)
    "social":      3,   # retail social buzz (StockTwits/Reddit) — often a fade
    "flavor":      5,   # moon phase / zodiac / date numerology (supplementary)
}

# ---- Edge thresholds (conservative profile) --------------------------------
MIN_CONVICTION   = 20.0   # |direction score - 50| * 2 must clear this to be a play
MAX_PICKS        = 5      # top-N plays per report
NEAR_MISS_BAND   = (10.0, 20.0)  # conviction range shown as "why NOT to trade"

# ---- Option selection -------------------------------------------------------
DTE_MIN, DTE_MAX     = 20, 45     # target expiry window (multi-week swing core)
OTM_PCT_CALL         = 0.03      # strike ≈ 3% above spot for calls
OTM_PCT_PUT          = 0.03      # strike ≈ 3% below spot for puts
CSP_OTM_PCT          = 0.05      # (kept for reference; CSP disabled below)
ALLOW_CSP            = False     # beginners only: simple long calls & puts, no cash-secured puts
MIN_OPEN_INTEREST    = 100
MAX_SPREAD_PCT       = 0.25      # (ask-bid)/mid must be under 25%
SMALL_ACCOUNT_BUDGET = 100.0     # contracts costing ≤ this get the "$100-friendly" tag
PREFER_CHEAP         = True      # surface low-cost, high-reward trades first (small accounts)
MAX_UNDERLYING_PRICE = 40.0      # focus the scan on low-priced stocks (little risk, big % upside)
HIGH_IV_HV_PCTL      = 80        # HV percentile above which we prefer selling premium (CSP)

# ---- Outcome grading --------------------------------------------------------
GRADE_WINDOW_DAYS  = 10          # trading days to judge a pick
WIN_MOVE_PCT       = 1.5         # underlying must move this % in our direction = WIN
DELTA_PROXY        = 0.40        # assumed option delta for premium P/L estimation

# ---- Output -----------------------------------------------------------------
PICKS_LOG   = "data/picks.csv"
REPORT_PATH = "docs/index.html"
TIMEZONE    = "US/Eastern"

# ---- Other markets watchlist (spot, no options) ----------------------------
# These trade in your broker's Crypto / Forex / Futures section, not as options.
# yfinance symbols; friendly names for the report.
WATCHLIST = {
    "crypto": [("BTC-USD", "Bitcoin"), ("ETH-USD", "Ethereum"), ("SOL-USD", "Solana"),
               ("XRP-USD", "XRP"), ("ADA-USD", "Cardano"), ("LINK-USD", "Chainlink"),
               ("AVAX-USD", "Avalanche"), ("LTC-USD", "Litecoin")],
    "forex":  [("EURUSD=X", "Euro / USD"), ("GBPUSD=X", "Pound / USD"),
               ("USDJPY=X", "USD / Yen"), ("AUDUSD=X", "Aussie / USD")],
    "commodities": [("GC=F", "Gold"), ("SI=F", "Silver"), ("CL=F", "Crude Oil"),
                    ("NG=F", "Natural Gas")],
}
# Meme coins — HIGH RISK, small-money lottery tickets. Never "low risk."
MEME_WATCH = [("DOGE-USD", "Dogecoin"), ("SHIB-USD", "Shiba Inu"), ("PEPE-USD", "Pepe"),
              ("WIF-USD", "dogwifhat"), ("FLOKI-USD", "Floki"), ("BONK-USD", "Bonk")]
WATCH_TOP = 4  # how many movers to surface per asset class
WATCH_TRADE_CONV = 24    # |score-50|*2 needed for an other-market mover to be a SUGGESTED trade
SPOT_POSITION_USD = 25   # flat suggested dollar size for a spot (crypto/forex/commodity) buy

# Tickers NOT tradeable on Robinhood — filtered out so every stock trade works there.
# Add any others you find unsupported.
ROBINHOOD_UNSUPPORTED = {"LCID", "AMC"}
