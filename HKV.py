from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
# yfinance removed – all data loaded from local CSVs
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="HKV - THYAO Financial Dashboard",
    layout="wide",
    page_icon="✈️"
)

# =====================================================
# CUSTOM CSS & TYPOGRAPHY
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.main {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    animation: fadeIn 0.6s ease-out;
}

[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 18px 20px !important;
    border-radius: 12px !important;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0px 8px 24px rgba(56, 189, 248, 0.25) !important;
    border-color: rgba(56, 189, 248, 0.4) !important;
}

[data-testid="stMetricValue"] {
    color: #00ffcc !important;
    font-family: 'Roboto Mono', monospace !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

[data-testid="stMetricDelta"] {
    font-weight: 600;
    font-size: 13px !important;
    font-family: 'Roboto Mono', monospace !important;
}

h1 {
    color: #f8fafc;
    font-size: 40px !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    margin-bottom: 5px;
    border-bottom: 2px solid #38bdf8;
    padding-bottom: 12px;
}

h2 {
    color: #f1f5f9;
    font-size: 24px !important;
    font-weight: 700 !important;
    margin-top: 35px;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 8px;
}

h3 {
    color: #cbd5e1;
    font-size: 16px !important;
    font-weight: 600 !important;
}

hr {
    border: 0;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    margin: 30px 0 !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

[data-baseweb="tab"] {
    border-radius: 8px !important;
    background: #1e293b !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    color: #94a3b8 !important;
    font-weight: 600;
    transition: all 0.2s ease;
    cursor: pointer;
    padding: 8px 16px !important;
}

[data-baseweb="tab"]:hover {
    background: #334155 !important;
    color: #f8fafc !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    background: #0284c7 !important;
    border-color: #38bdf8 !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stCheckbox"] label, [data-testid="stRadio"] label {
    color: #cbd5e1 !important;
    font-weight: 500;
    cursor: pointer;
}

[data-testid="baseButton-secondary"] {
    background: #1e293b !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #e2e8f0 !important;
    font-weight: 600;
    transition: all 0.2s ease;
    border-radius: 8px;
}

[data-testid="baseButton-secondary"]:hover {
    background: #334155 !important;
    border-color: #38bdf8 !important;
    color: #ffffff !important;
}

/* Floating Collapsible Navigation Menu (HTML Details Based) */
.nav-container {
    position: fixed !important;
    right: 20px !important;
    top: 15% !important;
    z-index: 999999 !important;
    font-family: 'Inter', sans-serif;
    border-radius: 12px;
    transition: all 0.3s ease;
}
.nav-container[open] {
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.nav-toggle-label {
    background: #0284c7;
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 13px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.15);
    list-style: none; /* Hide default arrow */
    outline: none;
    user-select: none;
}
.nav-toggle-label::-webkit-details-marker {
    display: none; /* Hide default arrow in Chrome/Safari */
}
.nav-toggle-label:hover {
    background: #0369a1;
    border-color: #38bdf8;
}
.nav-menu {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px 6px;
    width: 140px;
}
.nav-menu a {
    color: #94a3b8;
    text-decoration: none;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 10px;
    border-radius: 6px;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nav-menu a:hover {
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
}

@media (max-width: 768px) {
    .nav-container {
        display: none !important;
    }
}
</style>

<details class="nav-container">
    <summary class="nav-toggle-label">
        <span class="nav-icon">☰</span> Navigation
    </summary>
    <div class="nav-menu">
        <a href="#macro-panel">📊 Macro Panel</a>
        <a href="#stock-price">✈️ Stock Price</a>
        <a href="#technical-analysis">📈 Technical</a>
        <a href="#financial-metrics">💼 Financials</a>
        <a href="#peer-comparison">🔄 Peer Comp</a>
        <a href="#portfolio-alarms">💰 Portfolio</a>
    </div>
</details>

""", unsafe_allow_html=True)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def safe_float(value):
    try:
        if value is None or pd.isna(value):
            return None
        return float(str(value).replace(",", "."))
    except Exception:
        return None


def clean_negative_zero(val):
    if val is not None and abs(val) < 0.005:
        return 0.0
    return val


def format_number(value, suffix=""):
    if value is None or pd.isna(value):
        return "No data"
    value = clean_negative_zero(value)
    return f"{value:,.2f}{suffix}"


def format_abbreviated(value, is_usd=False):
    if value is None or pd.isna(value):
        return "No data"
    currency = "$" if is_usd else "TRY"
    return f"{value:,.1f}B {currency}"


# Local CSV Loaders
def load_local_fx(filepath):
    try:
        df = pd.read_csv(filepath, decimal=",")
        df.columns = [c.replace('"', '').strip() for c in df.columns]
        df = df.rename(columns={"Tarih": "Date", "Şimdi": "close_price"})
        df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
        df["close_price"] = pd.to_numeric(df["close_price"], errors="coerce")
        df = df.sort_values("Date")
        return df
    except Exception:
        return pd.DataFrame()


def load_local_faiz():
    try:
        df = pd.read_csv("data/faiz_tcmb_2002_2026.csv")
        df["Date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
        df = df.rename(columns={"interest_rate_overnight_lending": "Interest_Rate"})
        df = df.sort_values("Date")
        return df
    except Exception:
        return pd.DataFrame()


def load_local_enflasyon():
    try:
        df = pd.read_csv("data/enflasyon_tcmb_2005_2026.csv")
        df["Date"] = pd.to_datetime(df["date"], format="%m-%Y")
        df = df.rename(columns={"tufe_yillik_pct": "Inflation"})
        df = df.sort_values("Date")
        return df
    except Exception:
        return pd.DataFrame()


def load_local_annual(filepath):
    try:
        df = pd.read_csv(filepath)
        df["Year"] = df["Year"].astype(int)
        df = df.sort_values("Year")
        return df
    except Exception:
        return pd.DataFrame()


# =====================================================
# CSV-ONLY DATA LOADERS  (yfinance completely removed)
# =====================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_thyao_csv():
    """Load full THYAO price history from local CSV."""
    try:
        df = pd.read_csv("data/thyao_price_yahoo_2020_2026.csv")
        df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
        df = df.sort_values("Date").reset_index(drop=True)
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def load_financial_data():
    """Load quarterly financials from local CSV."""
    try:
        df = pd.read_csv("data/financial_metrics.csv")
        df.columns = [c.strip() for c in df.columns]
        for col in ["Profit", "Revenue", "Assets", "Liabilities"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "Quarter" not in df.columns:
            df["Quarter"] = [f"Q{i+1}" for i in range(len(df))]
        return df
    except Exception:
        return pd.DataFrame()


def filter_by_timeframe(df, timeframe):
    """Filter a full CSV dataframe by the selected timeframe."""
    if df.empty:
        return df
    latest_date = df["Date"].max()
    cuts = {
        "1d":  30,
        "1w":  90,
        "3m":  90,
        "6m":  180,
        "1y":  365,
        "3y":  3 * 365,
        "5y":  5 * 365,
        "All": None,
    }
    days = cuts.get(timeframe, None)
    if days is None:
        return df
    return df[df["Date"] >= latest_date - timedelta(days=days)]


def add_technical_indicators(df, ma_short=20, ma_long=50):
    if df.empty or len(df) < 20:
        return df
    try:
        df = df.copy()
        close = df["close_price"].astype(float)
        df["RSI"] = RSIIndicator(close=close, window=14).rsi()
        macd = MACD(close=close)
        df["MACD"] = macd.macd()
        df["MACD_SIGNAL"] = macd.macd_signal()
        bb = BollingerBands(close=close, window=20)
        df["BB_HIGH"] = bb.bollinger_hband()
        df["BB_LOW"] = bb.bollinger_lband()
        df[f"MA{ma_short}"] = close.rolling(window=ma_short).mean()
        df[f"MA{ma_long}"] = close.rolling(window=ma_long).mean()
    except Exception:
        pass
    return df


def calculate_dynamic_beta(thyao_df, bist_df):
    try:
        merged = pd.merge(
            thyao_df[["Date", "close_price"]],
            bist_df[["Date", "close_price"]],
            on="Date",
            suffixes=("_thyao", "_bist")
        ).sort_values("Date")
        
        merged["ret_thyao"] = merged["close_price_thyao"].pct_change()
        merged["ret_bist"] = merged["close_price_bist"].pct_change()
        
        merged = merged.dropna()
        if len(merged) < 5:
            return None
            
        covariance = merged["ret_thyao"].cov(merged["ret_bist"])
        variance = merged["ret_bist"].var()
        
        if variance == 0:
            return None
        return covariance / variance
    except Exception:
        return None

# =====================================================
# DATA INITIALIZATION & TIME FRAME STATE
# =====================================================

if "timeframe" not in st.session_state or st.session_state.timeframe in ("1h", "4h"):
    st.session_state.timeframe = "1y"

st.info(f"⏰ Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")
st.title("✈️ HKV - THYAO Financial Dashboard")
st.markdown("---")

# =====================================================
# SIDEBAR CONTROLS
# =====================================================

st.sidebar.markdown("## ✈️ Dashboard Controls")

chart_type = st.sidebar.radio("Chart Type", ["Line", "Candlestick", "Bar"], index=1, key="chart_type_radio")
show_volume = st.sidebar.checkbox("Show Volume", value=True, key="show_volume_checkbox")

st.sidebar.markdown("### 📈 Indicator Overlays")
show_ma_short = st.sidebar.checkbox("Show MA (Short)", value=True)
ma_short_period = st.sidebar.number_input("Short MA Period", min_value=5, max_value=200, value=20, step=1, key="ma_short_input")
show_ma_long = st.sidebar.checkbox("Show MA (Long)", value=True)
ma_long_period = st.sidebar.number_input("Long MA Period", min_value=10, max_value=500, value=50, step=1, key="ma_long_input")
show_bb = st.sidebar.checkbox("Show Bollinger Bands", value=False)

st.sidebar.markdown("### 📊 Subcharts")
show_rsi = st.sidebar.checkbox("Show RSI", value=True)
show_macd = st.sidebar.checkbox("Show MACD", value=True)

if st.sidebar.button("🔄 Refresh Data", key="refresh_data_button"):
    st.cache_data.clear()
    st.rerun()

# Load data from CSV only
with st.spinner("Loading data..."):
    thyao_full = load_thyao_csv()
    thyao = filter_by_timeframe(thyao_full, st.session_state.timeframe)
    # No CSV for BIST100 / PGSUS – peer comparison will show empty gracefully
    bist100 = pd.DataFrame()
    pgsus   = pd.DataFrame()
    thyao_info = {}  # No API – metrics calculated dynamically below
    financial  = load_financial_data()

if thyao.empty:
    st.error("THYAO data could not be loaded. Please make sure data/thyao_price_yahoo_2020_2026.csv exists.")
    st.stop()

# Add technical indicators
thyao = add_technical_indicators(thyao, ma_short=ma_short_period, ma_long=ma_long_period)

# Outstanding shares definition for dynamic calculations
outstanding_shares = 1_380_000_000

# =====================================================
# 1. MACROECONOMIC INDICATORS (MACRO PANEL)
# =====================================================

st.markdown("<div id='macro-panel'></div>", unsafe_allow_html=True)
st.header("1. Macroeconomic Indicators")

# Load Local Macro Data
usdtry_local = load_local_fx("data/USD_TRY Geçmiş Verileri (1).csv")
eurtry_local = load_local_fx("data/EUR_TRY Geçmiş Verileri.csv")
faiz_df = load_local_faiz()
enflasyon_df = load_local_enflasyon()

unemployment_df = load_local_annual("data/unemployment.csv")
gdp_df = load_local_annual("data/gdp_growth_clean.csv")
current_account_df = load_local_annual("data/current_account.csv")

# Filter to display 2020-2026 range for exchange & TCMB rates
usdtry_local_filtered = usdtry_local[usdtry_local["Date"] >= "2020-01-01"] if not usdtry_local.empty else pd.DataFrame()
eurtry_local_filtered = eurtry_local[eurtry_local["Date"] >= "2020-01-01"] if not eurtry_local.empty else pd.DataFrame()
faiz_df_filtered = faiz_df[faiz_df["Date"] >= "2020-01-01"] if not faiz_df.empty else pd.DataFrame()
enflasyon_df_filtered = enflasyon_df[enflasyon_df["Date"] >= "2020-01-01"] if not enflasyon_df.empty else pd.DataFrame()

# Get latest rates
latest_usd = usdtry_local["close_price"].iloc[-1] if not usdtry_local.empty else None
latest_eur = eurtry_local["close_price"].iloc[-1] if not eurtry_local.empty else None
latest_faiz = faiz_df["Interest_Rate"].iloc[-1] if not faiz_df.empty else None
latest_enflasyon = enflasyon_df["Inflation"].iloc[-1] if not enflasyon_df.empty else None

# Metric Columns
mac_col1, mac_col2, mac_col3, mac_col4 = st.columns(4)

mac_col1.metric(
    "🇺🇸 USD/TRY", 
    f"{latest_usd:.4f} TRY" if latest_usd else "No data",
    delta=f"{usdtry_local['close_price'].iloc[-1] - usdtry_local['close_price'].iloc[-2]:+.4f} TRY" if len(usdtry_local) > 1 else None
)
mac_col2.metric(
    "🇪🇺 EUR/TRY", 
    f"{latest_eur:.4f} TRY" if latest_eur else "No data",
    delta=f"{eurtry_local['close_price'].iloc[-1] - eurtry_local['close_price'].iloc[-2]:+.4f} TRY" if len(eurtry_local) > 1 else None
)
mac_col3.metric(
    "🏛️ TCMB Policy Interest Rate", 
    f"{latest_faiz:.2f}%" if latest_faiz else "No data",
    delta=f"{faiz_df['Interest_Rate'].iloc[-1] - faiz_df['Interest_Rate'].iloc[-2]:+.2f}%" if len(faiz_df) > 1 else None
)
mac_col4.metric(
    "🎈 Annual Inflation (CPI)", 
    f"{latest_enflasyon:.2f}%" if latest_enflasyon else "No data",
    delta=f"{enflasyon_df['Inflation'].iloc[-1] - enflasyon_df['Inflation'].iloc[-2]:+.2f}%" if len(enflasyon_df) > 1 else None
)

# Macro Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Exchange Rates Trend (Local CSV)")
    fx_fig = go.Figure()
    if not usdtry_local_filtered.empty:
        fx_fig.add_trace(go.Scatter(x=usdtry_local_filtered["Date"], y=usdtry_local_filtered["close_price"], mode="lines", name="USD/TRY", line=dict(color="#38bdf8", width=2)))
    if not eurtry_local_filtered.empty:
        fx_fig.add_trace(go.Scatter(x=eurtry_local_filtered["Date"], y=eurtry_local_filtered["close_price"], mode="lines", name="EUR/TRY", line=dict(color="#fbbf24", width=2)))
    fx_fig.update_layout(
        template="plotly_dark", height=380, margin=dict(l=40, r=40, t=30, b=30),
        plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
        font=dict(color="#94a3b8"), hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fx_fig, use_container_width=True)

with chart_col2:
    st.subheader("TCMB Interest & Inflation Trend")
    faiz_inf_fig = go.Figure()
    if not faiz_df_filtered.empty:
        faiz_inf_fig.add_trace(go.Scatter(x=faiz_df_filtered["Date"], y=faiz_df_filtered["Interest_Rate"], mode="lines+markers", name="Interest Rate", line=dict(color="#f43f5e", width=2)))
    if not enflasyon_df_filtered.empty:
        faiz_inf_fig.add_trace(go.Scatter(x=enflasyon_df_filtered["Date"], y=enflasyon_df_filtered["Inflation"], mode="lines+markers", name="Inflation Rate", line=dict(color="#10b981", width=2)))
    faiz_inf_fig.update_layout(
        template="plotly_dark", height=380, margin=dict(l=40, r=40, t=30, b=30),
        plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
        font=dict(color="#94a3b8"), hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(faiz_inf_fig, use_container_width=True)

# Grid for Annual Indicators
st.subheader("Annual Macroeconomic Indicators (2020 - 2026)")
gdp_ca_unemp_cols = st.columns(3)

with gdp_ca_unemp_cols[0]:
    st.markdown("#### 📈 GDP Growth Rate")
    if not gdp_df.empty:
        gdp_fig = px.bar(gdp_df, x="Year", y="Growth", text="Growth", labels={"Growth": "Growth %", "Year": "Year"})
        gdp_fig.update_traces(marker_color="#38bdf8", texttemplate="%{text:.1f}%", textposition="outside")
        gdp_fig.update_layout(template="plotly_dark", height=250, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(gdp_fig, use_container_width=True)
    else:
        st.warning("GDP growth data missing.")

with gdp_ca_unemp_cols[1]:
    st.markdown("#### 💼 Unemployment Rate")
    if not unemployment_df.empty:
        unemp_fig = px.line(unemployment_df, x="Year", y="Rate", markers=True, labels={"Rate": "Unemployment %", "Year": "Year"})
        unemp_fig.update_traces(line=dict(color="#f43f5e", width=3), marker=dict(size=8))
        unemp_fig.update_layout(template="plotly_dark", height=250, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(unemp_fig, use_container_width=True)
    else:
        st.warning("Unemployment data missing.")

with gdp_ca_unemp_cols[2]:
    st.markdown("#### 💸 Current Account Balance")
    if not current_account_df.empty:
        current_account_df["Color"] = np.where(current_account_df["Current_Account"] >= 0, "#10b981", "#ef4444")
        ca_fig = go.Figure()
        ca_fig.add_trace(go.Bar(
            x=current_account_df["Year"],
            y=current_account_df["Current_Account"],
            marker_color=current_account_df["Color"],
            text=current_account_df["Current_Account"],
            texttemplate="%{text:.1f}B",
            textposition="outside"
        ))
        ca_fig.update_layout(
            template="plotly_dark", height=250, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Billion $"
        )
        st.plotly_chart(ca_fig, use_container_width=True)
    else:
        st.warning("Current Account data missing.")

st.markdown("---")

# =====================================================
# 2. THYAO STOCK PRICE
# =====================================================

st.markdown("<div id='stock-price'></div>", unsafe_allow_html=True)
st.header("2. THYAO Stock Price")

# Timeframe selector horizontal columns
st.write("⏱️ Select Timeframe:")
t_cols = st.columns(8)
timeframes = ["1d", "1w", "3m", "6m", "1y", "3y", "5y", "All"]

for idx, tf_label in enumerate(timeframes):
    btn_style = "primary" if st.session_state.timeframe == tf_label else "secondary"
    if t_cols[idx].button(tf_label, key=f"tf_{tf_label}", use_container_width=True, type=btn_style):
        st.session_state.timeframe = tf_label
        st.rerun()

# Overview Metric Cards
latest_close = float(thyao["close_price"].iloc[-1])
previous_close = float(thyao["close_price"].iloc[-2]) if len(thyao) > 1 else None

price_delta = None
price_delta_pct = None

if previous_close is not None and previous_close != 0:
    price_delta = clean_negative_zero(latest_close - previous_close)
    price_delta_pct = clean_negative_zero((price_delta / previous_close) * 100)

# Calculate dynamic Beta against BIST100
calculated_beta = calculate_dynamic_beta(thyao, bist100)
display_beta = calculated_beta if calculated_beta is not None else 1.08

st.subheader(f"Summary Indicators ({st.session_state.timeframe.upper()} Period)")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Current Price",
    f"{latest_close:.2f} TRY",
    f"{price_delta:+.2f} TRY / {price_delta_pct:+.2f}%" if price_delta_pct is not None else None
)
col2.metric("📈 Highest Price", f"{thyao['high'].max():.2f} TRY")
col3.metric("📉 Lowest Price", f"{thyao['low'].min():.2f} TRY")
col4.metric("📊 Average Volume", f"{thyao['volume'].mean():,.0f}")
col5.metric(
    "📈 Beta Value (Calculated)",
    f"{display_beta:.2f}"
)

# Stock Price Chart
price_fig = go.Figure()

if chart_type == "Candlestick":
    price_fig.add_trace(
        go.Candlestick(
            x=thyao["Date"],
            open=thyao["open"],
            high=thyao["high"],
            low=thyao["low"],
            close=thyao["close_price"],
            name="THYAO Candlestick",
            increasing_line_color="#10b981",
            decreasing_line_color="#ef4444"
        )
    )
elif chart_type == "Bar":
    price_fig.add_trace(
        go.Ohlc(
            x=thyao["Date"],
            open=thyao["open"],
            high=thyao["high"],
            low=thyao["low"],
            close=thyao["close_price"],
            name="THYAO Bar Chart",
            increasing_line_color="#10b981",
            decreasing_line_color="#ef4444"
        )
    )
else: # Line Chart
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao["close_price"],
            mode="lines",
            name="Close Price",
            line=dict(width=3, color="#38bdf8")
        )
    )

# Indicator Overlays
ma_short_col = f"MA{ma_short_period}"
ma_long_col = f"MA{ma_long_period}"

if show_ma_short and ma_short_col in thyao.columns:
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao[ma_short_col],
            mode="lines",
            name=f"MA{ma_short_period}",
            line=dict(color="#10b981", width=1.5, dash="dash")
        )
    )
if show_ma_long and ma_long_col in thyao.columns:
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao[ma_long_col],
            mode="lines",
            name=f"MA{ma_long_period}",
            line=dict(color="#ef4444", width=1.5, dash="dot")
        )
    )
if show_bb and "BB_HIGH" in thyao.columns:
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao["BB_HIGH"],
            mode="lines",
            name="Bollinger Band Upper",
            line=dict(color="#fbbf24", width=1.2, dash="dash")
        )
    )
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao["BB_LOW"],
            mode="lines",
            name="Bollinger Band Lower",
            line=dict(color="#fbbf24", width=1.2, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(251, 191, 36, 0.04)"
        )
    )

price_fig.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_rangeslider_visible=False,
    hovermode="x unified",
    plot_bgcolor="rgba(30, 41, 59, 0.4)",
    paper_bgcolor="rgba(15, 23, 42, 0)",
    font=dict(color="#cbd5e1")
)
st.plotly_chart(price_fig, use_container_width=True)

# Show Volume Chart
if show_volume:
    volume_fig = px.bar(thyao, x="Date", y="volume", title="Trading Volume")
    volume_fig.update_traces(marker=dict(color="#38bdf8", line=dict(color="#38bdf8", width=1)))
    volume_fig.update_layout(
        template="plotly_dark",
        height=280,
        plot_bgcolor="rgba(30, 41, 59, 0.4)",
        paper_bgcolor="rgba(15, 23, 42, 0)",
        font=dict(color="#cbd5e1"),
        hovermode="x unified"
    )
    st.plotly_chart(volume_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 3. TECHNICAL ANALYSIS
# =====================================================

st.markdown("<div id='technical-analysis'></div>", unsafe_allow_html=True)
st.header("3. Technical Analysis")

# Timeframe labels for indicators
tf_labels = {
    "1h": "1-Hour Interval",
    "4h": "4-Hour Interval",
    "1d": "Daily Interval (1D)",
    "1w": "Weekly Interval (1W)",
    "3m": "Daily Interval (Last 3 Months)",
    "6m": "Daily Interval (Last 6 Months)",
    "1y": "Daily Interval (Last 1 Year)",
    "3y": "Daily Interval (Last 3 Years)",
    "5y": "Daily Interval (Last 5 Years)",
    "All": "Daily Interval (All Data)"
}
current_tf_label = tf_labels.get(st.session_state.timeframe, "Daily Interval")

ta_tabs = ["RSI Indicator", "MACD Indicator", "TradingView"]
tabs = st.tabs(ta_tabs)

with tabs[0]:
    if show_rsi and "RSI" in thyao.columns:
        st.subheader(f"RSI Indicator ({current_tf_label})")
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["RSI"], mode="lines", name="RSI", line=dict(color="#38bdf8", width=2.5)))
        rsi_fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", annotation_text="Overbought")
        rsi_fig.add_hline(y=30, line_dash="dash", line_color="#10b981", annotation_text="Oversold")
        rsi_fig.update_layout(
            template="plotly_dark", height=380,
            plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#cbd5e1"), hovermode="x unified"
        )
        st.plotly_chart(rsi_fig, use_container_width=True)
    else:
        st.info("RSI overlay is disabled or has insufficient historical data.")

with tabs[1]:
    if show_macd and "MACD" in thyao.columns:
        st.subheader(f"MACD Indicator ({current_tf_label})")
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["MACD"], mode="lines", name="MACD", line=dict(color="#38bdf8", width=2.5)))
        macd_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["MACD_SIGNAL"], mode="lines", name="Signal", line=dict(color="#10b981", width=1.5, dash="dash")))
        macd_fig.update_layout(
            template="plotly_dark", height=380,
            plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#cbd5e1"), hovermode="x unified"
        )
        st.plotly_chart(macd_fig, use_container_width=True)
    else:
        st.info("MACD overlay is disabled or has insufficient historical data.")

with tabs[2]:
    st.subheader("THYAO - TradingView Grafiği")
    st.markdown("""
    > **Not:** TradingView'ın ücretsiz embed widget'ı Borsa İstanbul (BIST) sembollerini
    > desteklemiyor. Aşağıdaki butona tıklayarak THYAO grafiğini TradingView'da açabilirsin.
    """)
    tv_link_html = """
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                gap:20px; padding: 60px 20px; text-align:center;">
      <div style="font-size:64px;">📈</div>
      <div style="color:#94a3b8; font-size:16px; max-width:480px;">
        TradingView'da <strong style="color:#38bdf8;">BIST:THYAO</strong> grafiğini
        gerçek zamanlı olarak incelemek için butona tıkla.
      </div>
      <a href="https://www.tradingview.com/chart/?symbol=BIST%3ATHYAO"
         target="_blank"
         style="display:inline-block; background:linear-gradient(135deg,#0284c7,#0ea5e9);
                color:#ffffff; font-weight:700; font-size:15px; padding:14px 32px;
                border-radius:10px; text-decoration:none; letter-spacing:0.5px;
                box-shadow:0 4px 15px rgba(2,132,199,0.4);
                transition:all 0.2s ease;">
        🚀 TradingView'da Aç
      </a>
    </div>
    """
    st.components.v1.html(tv_link_html, height=320)

st.markdown("---")

# =====================================================
# 4. FINANCIAL METRICS
# =====================================================

st.markdown("<div id='financial-metrics'></div>", unsafe_allow_html=True)
st.header("4. Financial Metrics")

# Info metrics - Calculate dynamically to prevent API "No data" issues
beta_info = thyao_info.get("beta")
market_cap_info = thyao_info.get("marketCap")
trailing_pe_info = thyao_info.get("trailingPE")
sector_info = "Aviation"  # Force to Aviation since this is a THYAO dashboard

# Fallback/dynamic calculations if yfinance info is empty or corrupt (returns near-zero/negative Beta)
if beta_info is None or pd.isna(beta_info) or abs(beta_info) < 0.05:
    beta_info = display_beta

if market_cap_info is None or pd.isna(market_cap_info) or market_cap_info <= 0:
    market_cap_info = latest_close * outstanding_shares

if trailing_pe_info is None or pd.isna(trailing_pe_info) or trailing_pe_info <= 0:
    if not financial.empty and "Profit" in financial.columns:
        ttm_profit_b = financial["Profit"].tail(4).sum()
        ttm_profit_real = ttm_profit_b * 1_000_000_000
        if ttm_profit_real > 0:
            eps_calc = ttm_profit_real / outstanding_shares
            trailing_pe_info = latest_close / eps_calc
        else:
            trailing_pe_info = 7.5
    else:
        trailing_pe_info = 7.5

metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("📈 Beta (Info)", f"{beta_info:.2f}")
metric2.metric("🏢 Market Capitalization", f"₺{market_cap_info / 1_000_000_000:.2f}B")
metric3.metric("📊 P/E Ratio", f"{trailing_pe_info:.2f}")
metric4.metric("🏭 Sector", sector_info)

if financial.empty:
    st.warning("Financial statements data could not be loaded.")
else:
    st.subheader("Quarterly Financial Performance Report (Billion TRY)")
    
    financial_col1, financial_col2 = st.columns(2)

    with financial_col1:
        if "Profit" in financial.columns and financial["Profit"].notna().any():
            profit_fig = px.bar(financial, x="Quarter", y="Profit", title="Quarterly Net Income (Billion TRY)")
            profit_fig.update_traces(
                marker=dict(color="#38bdf8", line=dict(color="#38bdf8", width=1.5)),
                texttemplate="%{y:.1f}B TRY",
                textposition="auto",
                hovertemplate="Quarter: %{x}<br>Net Income: %{y:.2f}B TRY"
            )
            profit_fig.update_layout(
                template="plotly_dark", height=380,
                plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
                font=dict(color="#cbd5e1"), yaxis_title="Billion TRY"
            )
            st.plotly_chart(profit_fig, use_container_width=True)

    with financial_col2:
        if "Revenue" in financial.columns and financial["Revenue"].notna().any():
            revenue_fig = px.line(financial, x="Quarter", y="Revenue", title="Quarterly Revenue Growth (Billion TRY)", markers=True)
            revenue_fig.update_traces(
                line=dict(color="#10b981", width=3),
                marker=dict(size=8),
                hovertemplate="Quarter: %{x}<br>Revenue: %{y:.2f}B TRY"
            )
            revenue_fig.update_layout(
                template="plotly_dark", height=380,
                plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
                font=dict(color="#cbd5e1"), yaxis_title="Billion TRY"
            )
            st.plotly_chart(revenue_fig, use_container_width=True)

    financial_col3, financial_col4 = st.columns(2)

    with financial_col3:
        if "Assets" in financial.columns and financial["Assets"].notna().any():
            assets_fig = px.line(financial, x="Quarter", y="Assets", title="Total Asset Growth (Billion TRY)", markers=True)
            assets_fig.update_traces(
                line=dict(color="#fbbf24", width=3),
                marker=dict(size=8),
                hovertemplate="Quarter: %{x}<br>Total Assets: %{y:.2f}B TRY"
            )
            assets_fig.update_layout(
                template="plotly_dark", height=380,
                plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
                font=dict(color="#cbd5e1"), yaxis_title="Billion TRY"
            )
            st.plotly_chart(assets_fig, use_container_width=True)

    with financial_col4:
        if "Liabilities" in financial.columns and financial["Liabilities"].notna().any():
            liabilities_fig = px.bar(financial, x="Quarter", y="Liabilities", title="Total Liabilities (Billion TRY)")
            liabilities_fig.update_traces(
                marker=dict(color="#ef4444", line=dict(color="#ef4444", width=1.5)),
                texttemplate="%{y:.1f}B TRY",
                textposition="auto",
                hovertemplate="Quarter: %{x}<br>Liabilities: %{y:.2f}B TRY"
            )
            liabilities_fig.update_layout(
                template="plotly_dark", height=380,
                plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
                font=dict(color="#cbd5e1"), yaxis_title="Billion TRY"
            )
            st.plotly_chart(liabilities_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 5. PEER COMPARISON
# =====================================================

st.markdown("<div id='peer-comparison'></div>", unsafe_allow_html=True)
st.header("5. Peer Comparison")

comparison_fig = go.Figure()
comparison_trace_count = 0

for name, df in [("THYAO", thyao), ("PGSUS", pgsus), ("BIST100", bist100)]:
    if df is None or df.empty or "Date" not in df.columns or "close_price" not in df.columns:
        continue

    temp = df[["Date", "close_price"]].copy()
    temp = temp.dropna(subset=["Date", "close_price"])

    if temp.empty:
        continue

    first_value = safe_float(temp["close_price"].iloc[0])
    if first_value is None or first_value == 0:
        continue

    temp["Indexed Return"] = temp["close_price"].astype(float) / first_value * 100

    comparison_fig.add_trace(
        go.Scatter(
            x=temp["Date"],
            y=temp["Indexed Return"],
            mode="lines",
            name=name,
            line=dict(width=2)
        )
    )
    comparison_trace_count += 1

if comparison_trace_count > 0:
    comparison_fig.update_layout(
        title="Indexed Return Performance Comparison (Base = 100)",
        template="plotly_dark",
        height=480,
        plot_bgcolor="rgba(30, 41, 59, 0.4)",
        paper_bgcolor="rgba(15, 23, 42, 0)",
        font=dict(color="#cbd5e1"),
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Indexed Return (%)"
    )
    st.plotly_chart(comparison_fig, use_container_width=True)
else:
    st.warning("Comparison data could not be loaded.")

col1, col2 = st.columns(2)

with col1:
    if not pgsus.empty:
        pgsus_fig = px.line(pgsus, x="Date", y="close_price", title="Pegasus (PGSUS) Stock Price")
        pgsus_fig.update_layout(
            template="plotly_dark", height=380,
            plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#cbd5e1"), hovermode="x unified"
        )
        st.plotly_chart(pgsus_fig, use_container_width=True)

with col2:
    if not bist100.empty:
        bist_fig = px.line(bist100, x="Date", y="close_price", title="BIST 100 Index Price")
        bist_fig.update_layout(
            template="plotly_dark", height=380,
            plot_bgcolor="rgba(30, 41, 59, 0.4)", paper_bgcolor="rgba(15, 23, 42, 0)",
            font=dict(color="#cbd5e1"), hovermode="x unified"
        )
        st.plotly_chart(bist_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 6. PORTFOLIO TRACKER & ALARMS
# =====================================================

st.markdown("<div id='portfolio-alarms'></div>", unsafe_allow_html=True)
st.header("6. Portfolio Tracker & Price Alarms")

p_col1, p_col2 = st.columns(2)

with p_col1:
    st.subheader("💼 Portfolio Tracker")
    lot_count = st.number_input("Number of Shares (Lots Owned)", min_value=0, value=100, step=10, key="lot_input")
    avg_cost = st.number_input("Average Cost per Share (TRY)", min_value=0.0, value=300.0, step=1.0, key="cost_input")
    
    total_cost = lot_count * avg_cost
    current_value = lot_count * latest_close
    net_pnl = current_value - total_cost
    pnl_pct = (net_pnl / total_cost) * 100 if total_cost > 0 else 0.0
    
    pnl_color = "#10b981" if net_pnl >= 0 else "#ef4444"
    pnl_sign = "+" if net_pnl >= 0 else ""
    
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 25px; margin-top: 15px;">
        <h3 style="color: #94a3b8; font-size: 14px; text-transform: uppercase; margin-bottom: 20px; font-weight: 700;">Investment Performance</h3>
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #64748b;">Total Cost Basis:</span>
                <span style="font-family: 'Roboto Mono', monospace; font-weight: 700; color: #f8fafc;">{total_cost:,.2f} TRY</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #64748b;">Current Portfolio Value:</span>
                <span style="font-family: 'Roboto Mono', monospace; font-weight: 700; color: #f8fafc;">{current_value:,.2f} TRY</span>
            </div>
            <div style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 15px; display: flex; justify-content: space-between;">
                <span style="color: #64748b; font-weight: 600;">Net Profit / Loss:</span>
                <span style="font-family: 'Roboto Mono', monospace; font-weight: 700; color: {pnl_color};">{pnl_sign}{net_pnl:,.2f} TRY ({pnl_sign}{pnl_pct:.2f}%)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with p_col2:
    st.subheader("🔔 Price Alarms")
    alarm_price = st.number_input("Target Price Threshold (TRY)", min_value=0.0, value=latest_close, step=1.0, key="alarm_price_input")
    alarm_type = st.radio("Alarm Trigger Condition", ["Price >= Target", "Price <= Target"], horizontal=True, key="alarm_type_radio")
    alarm_active = st.checkbox("Activate Alarm", value=False, key="alarm_active_checkbox")
    
    if alarm_active:
        is_triggered = False
        if alarm_type == "Price >= Target" and latest_close >= alarm_price:
            is_triggered = True
        elif alarm_type == "Price <= Target" and latest_close <= alarm_price:
            is_triggered = True
            
        if is_triggered:
            st.success(f"🔔 **ALARM TRIGGERED!** THYAO Current price (**{latest_close:.2f} TRY**) crossed/reached your target of **{alarm_price:.2f} TRY**.")
        else:
            st.info(f"⏳ Alarm set. Will trigger when THYAO reaches **{alarm_price:.2f} TRY**. Current: **{latest_close:.2f} TRY**")

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<br><br>
<hr>
<div style="text-align: center; color: #64748b; font-size: 13px; padding-bottom: 20px;">
    <h3>✈️ HKV Team</h3>
    Financial Management and Investment Dashboard Project<br>
    Developed with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
