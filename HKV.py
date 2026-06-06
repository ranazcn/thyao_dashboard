from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
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
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
* {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.main {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    animation: fadeIn 0.6s ease-out;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2a5f8a;
    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0px 4px 16px rgba(52, 152, 219, 0.3);
    border-color: #3498db;
}

[data-testid="stMetricValue"] {
    color: #ecf0f1;
    font-size: 32px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

[data-testid="stMetricLabel"] {
    color: #95a5a6;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

[data-testid="stMetricDelta"] {
    color: #2ecc71;
    font-weight: 600;
    font-size: 14px;
}

h1 {
    color: #ecf0f1;
    font-size: 48px !important;
    font-weight: 700 !important;
    letter-spacing: 0px;
    margin-bottom: 5px;
}

h2 {
    color: #bdc3c7;
    font-size: 28px !important;
    font-weight: 700 !important;
    margin-top: 35px;
    margin-bottom: 20px;
    letter-spacing: 0px;
    border-bottom: 2px solid #2a5f8a;
    padding-bottom: 10px;
}

h3 {
    color: #95a5a6;
    font-size: 16px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
}

hr {
    border: 1px solid #2a5f8a;
    margin: 30px 0 !important;
    opacity: 0.5;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

[data-baseweb="tab"] {
    border-radius: 8px !important;
    background: #0f3460 !important;
    border: 1px solid #2a5f8a !important;
    color: #bdc3c7 !important;
    font-weight: 600;
    transition: all 0.2s ease;
    cursor: pointer;
}

[data-baseweb="tab"]:hover {
    background: #16213e !important;
    border-color: #3498db !important;
    color: #ecf0f1 !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    background: #1f4788 !important;
    border-color: #3498db !important;
    color: #ecf0f1 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%);
    border-right: 1px solid #2a5f8a;
}

[data-testid="stCheckbox"] label, [data-testid="stRadio"] label {
    color: #bdc3c7 !important;
    font-weight: 600;
    transition: all 0.2s ease;
    cursor: pointer;
}

[data-testid="stCheckbox"] label:hover, [data-testid="stRadio"] label:hover {
    color: #ecf0f1 !important;
}

[data-testid="baseButton-secondary"] {
    background: #0f3460 !important;
    border: 1px solid #2a5f8a !important;
    color: #bdc3c7 !important;
    font-weight: 600;
    transition: all 0.2s ease;
}

[data-testid="baseButton-secondary"]:hover {
    background: #16213e !important;
    border-color: #3498db !important;
    color: #ecf0f1 !important;
}

[data-testid="stSubheaderMain"] {
    color: #bdc3c7;
    font-weight: 700;
    letter-spacing: 0.5px;
}

input, button, select, textarea {
    transition: all 0.2s ease;
}

input:focus, button:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #3498db !important;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1) !important;
}

p, label, span {
    color: #bdc3c7;
}
</style>
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


def format_number(value, suffix=""):
    if value is None or pd.isna(value):
        return "No data"
    return f"{value:,.2f}{suffix}"


@st.cache_data(ttl=3600, show_spinner=False)
def load_yahoo_history(symbol, start="2020-01-01", period=None, interval="1d"):
    try:
        if period:
            df = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=False)
        else:
            df = yf.download(symbol, start=start, interval=interval, progress=False, auto_adjust=False)

        if df is None or df.empty:
            return pd.DataFrame()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close_price",
            "Adj Close": "adj_close",
            "Volume": "volume"
        })

        if "Date" not in df.columns and "Datetime" in df.columns:
            df = df.rename(columns={"Datetime": "Date"})

        df["Date"] = pd.to_datetime(df["Date"])
        return df

    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def load_yahoo_info(symbol):
    try:
        return yf.Ticker(symbol).info or {}
    except Exception:
        return {}


@st.cache_data(ttl=3600, show_spinner=False)
def load_yahoo_financials(symbol):
    try:
        ticker = yf.Ticker(symbol)
        income = ticker.quarterly_financials
        balance = ticker.quarterly_balance_sheet

        rows = []
        all_cols = sorted(set(list(income.columns) + list(balance.columns)))

        for col in all_cols:
            revenue = income.loc["Total Revenue", col] if "Total Revenue" in income.index and col in income.columns else None
            profit = income.loc["Net Income", col] if "Net Income" in income.index and col in income.columns else None
            assets = balance.loc["Total Assets", col] if "Total Assets" in balance.index and col in balance.columns else None
            liabilities = balance.loc["Total Liabilities Net Minority Interest", col] if "Total Liabilities Net Minority Interest" in balance.index and col in balance.columns else None

            revenue_f = safe_float(revenue)
            profit_f = safe_float(profit)
            assets_f = safe_float(assets)
            liabilities_f = safe_float(liabilities)

            col_date = pd.to_datetime(col)

            rows.append({
                "Quarter": f"{col_date.year}-Q{col_date.quarter}",
                "Date": col_date,
                "Revenue": revenue_f / 1_000_000_000 if revenue_f is not None else None,
                "Profit": profit_f / 1_000_000_000 if profit_f is not None else None,
                "Assets": assets_f / 1_000_000_000 if assets_f is not None else None,
                "Liabilities": liabilities_f / 1_000_000_000 if liabilities_f is not None else None,
            })

        df = pd.DataFrame(rows).dropna(how="all", subset=["Revenue", "Profit", "Assets", "Liabilities"])
        if not df.empty:
            df = df.sort_values("Date")
            df["Quarter"] = df["Date"].dt.year.astype(str) + "-Q" + df["Date"].dt.quarter.astype(str)
        return df

    except Exception:
        return pd.DataFrame()


# =====================================================
# DATA LOADING - YAHOO FINANCE API
# =====================================================

st.info(f"⏰ Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")
st.title("✈️ HKV - THYAO Financial Dashboard")
st.markdown("---")

with st.spinner("Fetching market data..."):
    thyao = load_yahoo_history("THYAO.IS", start="2020-01-01")
    usdtry = load_yahoo_history("USDTRY=X", start="2020-01-01")
    eurtry = load_yahoo_history("EURTRY=X", start="2020-01-01")
    gold = load_yahoo_history("GC=F", start="2020-01-01")
    brent = load_yahoo_history("BZ=F", start="2020-01-01")
    bist100 = load_yahoo_history("XU100.IS", start="2020-01-01")
    pgsus = load_yahoo_history("PGSUS.IS", start="2020-01-01")
    thyao_info = load_yahoo_info("THYAO.IS")
    financial = load_yahoo_financials("THYAO.IS")


if thyao.empty:
    st.error("THYAO data could not be loaded. Please check your internet connection, yfinance installation, or the THYAO.IS symbol.")
    st.stop()

required_cols = ["Date", "open", "high", "low", "close_price", "volume"]
missing_cols = [col for col in required_cols if col not in thyao.columns]
if missing_cols:
    st.error(f"The market data did not include the expected columns. Missing columns: {missing_cols}")
    st.stop()

# Teknik indikatörler
close = thyao["close_price"].astype(float)

thyao["RSI"] = RSIIndicator(close=close, window=14).rsi()
macd = MACD(close=close)
thyao["MACD"] = macd.macd()
thyao["MACD_SIGNAL"] = macd.macd_signal()
bb = BollingerBands(close=close, window=20)
thyao["BB_HIGH"] = bb.bollinger_hband()
thyao["BB_LOW"] = bb.bollinger_lband()
thyao["MA20"] = close.rolling(window=20).mean()
thyao["MA50"] = close.rolling(window=50).mean()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("## ✈️ Dashboard Controls")
st.sidebar.success("Market data is being loaded")

available_years = sorted(thyao["Date"].dt.year.dropna().astype(int).unique().tolist())
year_options = ["All"] + [str(year) for year in available_years]
selected_year_raw = st.sidebar.selectbox("Select Year", year_options, index=0, key="year_filter_selectbox")
selected_year = str(selected_year_raw) if selected_year_raw is not None else "All"
chart_type = st.sidebar.radio("Chart Type", ["Line", "Candlestick"], key="chart_type_radio")
show_volume = st.sidebar.checkbox("Show Volume", value=True, key="show_volume_checkbox")
show_ma = st.sidebar.checkbox("Show Moving Averages", value=True, key="show_ma_checkbox")

if st.sidebar.button("🔄 Refresh Data", key="refresh_data_button"):
    st.cache_data.clear()
    st.rerun()

if selected_year != "All":
    selected_year_int = int(selected_year)
    thyao = thyao[thyao["Date"].dt.year == selected_year_int]

if thyao.empty:
    st.warning("No THYAO data found for the selected year.")
    st.stop()

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("Overview Metrics")

latest_close = float(thyao["close_price"].iloc[-1])
previous_close = float(thyao["close_price"].iloc[-2]) if len(thyao) > 1 else None

price_delta = None
price_delta_pct = None

if previous_close is not None and previous_close != 0:
    price_delta = latest_close - previous_close
    price_delta_pct = (price_delta / previous_close) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Current Price",
    f"{latest_close:.2f} ₺",
    f"{price_delta:+.2f} ₺ / {price_delta_pct:+.2f}%" if price_delta_pct is not None else None
)
col2.metric("📈 Highest Price", f"{thyao['high'].max():.2f} ₺")
col3.metric("📉 Lowest Price", f"{thyao['low'].min():.2f} ₺")
col4.metric("📊 Average Volume", f"{thyao['volume'].mean():,.0f}")

st.markdown("---")

# =====================================================
# 1. LIVE MARKET DATA PANEL
# =====================================================

st.header("1. Live Market Data Panel")

m1, m2, m3, m4 = st.columns(4)

m1.metric("THYAO", f"{latest_close:.2f} ₺")
m2.metric("USD/TRY", f"{usdtry['close_price'].iloc[-1]:.2f} ₺" if not usdtry.empty else "No data")
m3.metric("EUR/TRY", f"{eurtry['close_price'].iloc[-1]:.2f} ₺" if not eurtry.empty else "No data")
m4.metric("Gold Futures", f"${gold['close_price'].iloc[-1]:.2f}" if not gold.empty else "No data")

col1, col2 = st.columns(2)

with col1:
    if not usdtry.empty:
        usd_fig = px.line(usdtry, x="Date", y="close_price", title="USD/TRY")
        usd_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"))
        st.plotly_chart(usd_fig, use_container_width=True)
    else:
        st.warning("USD/TRY data could not be loaded.")

with col2:
    if not gold.empty:
        gold_fig = px.line(gold, x="Date", y="close_price", title="Gold Futures")
        gold_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"))
        st.plotly_chart(gold_fig, use_container_width=True)
    else:
        st.warning("Gold data could not be loaded.")

col1, col2 = st.columns(2)

with col1:
    if not eurtry.empty:
        eur_fig = px.line(eurtry, x="Date", y="close_price", title="EUR/TRY")
        eur_fig.update_layout(template="plotly_dark", height=350, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"))
        st.plotly_chart(eur_fig, use_container_width=True)

with col2:
    if not brent.empty:
        brent_fig = px.line(brent, x="Date", y="close_price", title="Brent Oil Futures")
        brent_fig.update_layout(template="plotly_dark", height=350, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"))
        st.plotly_chart(brent_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 2. THYAO STOCK PRICE
# =====================================================

st.header("2. THYAO Stock Price")

price_fig = go.Figure()

if chart_type == "Candlestick":
    price_fig.add_trace(
        go.Candlestick(
            x=thyao["Date"],
            open=thyao["open"],
            high=thyao["high"],
            low=thyao["low"],
            close=thyao["close_price"],
            name="THYAO",
            increasing_line_color="#2ecc71",
            decreasing_line_color="#e74c3c"
        )
    )
else:
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao["close_price"],
            mode="lines",
            name="Close Price",
            line=dict(width=3, color="#3498db")
        )
    )

if show_ma:
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao["MA20"],
            mode="lines",
            name="MA20",
            line=dict(color="#2ecc71", width=2, dash="dash")
        )
    )
    price_fig.add_trace(
        go.Scatter(
            x=thyao["Date"],
            y=thyao["MA50"],
            mode="lines",
            name="MA50",
            line=dict(color="#e74c3c", width=2, dash="dot")
        )
    )

price_fig.update_layout(
    template="plotly_dark",
    height=650,
    xaxis_rangeslider_visible=False,
    hovermode="x unified",
    plot_bgcolor="#16213e",
    paper_bgcolor="#0f1a2e",
    font=dict(color="#ecf0f1")
)
st.plotly_chart(price_fig, use_container_width=True)

if show_volume:
    volume_fig = px.bar(thyao, x="Date", y="volume", title="Trading Volume")
    volume_fig.update_traces(marker=dict(color="#3498db", line=dict(color="#3498db", width=1)))
    volume_fig.update_layout(template="plotly_dark", height=350, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
    st.plotly_chart(volume_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 3. TECHNICAL ANALYSIS
# =====================================================

st.header("3. Technical Analysis")

tab1, tab2, tab3 = st.tabs(["RSI", "MACD", "Bollinger Bands"])

with tab1:
    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["RSI"], mode="lines", name="RSI", line=dict(color="#3498db", width=3)))
    rsi_fig.add_hline(y=70, line_dash="dash", line_color="#e74c3c", annotation_text="Overbought")
    rsi_fig.add_hline(y=30, line_dash="dash", line_color="#2ecc71", annotation_text="Oversold")
    rsi_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
    st.plotly_chart(rsi_fig, use_container_width=True)

with tab2:
    macd_fig = go.Figure()
    macd_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["MACD"], mode="lines", name="MACD", line=dict(color="#3498db", width=3)))
    macd_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["MACD_SIGNAL"], mode="lines", name="Signal", line=dict(color="#2ecc71", width=2, dash="dash")))
    macd_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
    st.plotly_chart(macd_fig, use_container_width=True)

with tab3:
    bollinger_fig = go.Figure()
    bollinger_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["close_price"], mode="lines", name="Close Price", line=dict(color="#3498db", width=3)))
    bollinger_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["BB_HIGH"], mode="lines", name="Upper Band", line=dict(color="#e74c3c", dash="dash", width=2)))
    bollinger_fig.add_trace(go.Scatter(x=thyao["Date"], y=thyao["BB_LOW"], mode="lines", name="Lower Band", line=dict(color="#2ecc71", dash="dash", width=2), fill="tonexty", fillcolor="rgba(46, 204, 113, 0.1)"))
    bollinger_fig.update_layout(template="plotly_dark", height=450, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
    st.plotly_chart(bollinger_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 4. FINANCIAL METRICS - YAHOO FINANCE
# =====================================================

st.header("4. Financial Metrics")

beta = thyao_info.get("beta")
market_cap = thyao_info.get("marketCap")
trailing_pe = thyao_info.get("trailingPE")
sector = thyao_info.get("sector", "No data")

metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("📈 Beta", f"{beta:.2f}" if beta is not None else "No data")
metric2.metric("🏢 Market Cap", f"₺{market_cap / 1_000_000_000:.1f}B" if market_cap else "No data")
metric3.metric("📊 P/E Ratio", f"{trailing_pe:.2f}" if trailing_pe else "No data")
metric4.metric("🏭 Sector", sector)

if financial.empty:
    st.warning("Financial statements could not be loaded. Stock price and technical analysis sections will continue to work.")
else:
    financial_col1, financial_col2 = st.columns(2)

    with financial_col1:
        if "Profit" in financial.columns and financial["Profit"].notna().any():
            profit_fig = px.bar(financial, x="Quarter", y="Profit", title="Quarterly Profit / Net Income")
            profit_fig.update_traces(marker=dict(color="#3498db", line=dict(color="#3498db", width=2)))
            profit_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
            st.plotly_chart(profit_fig, use_container_width=True)

    with financial_col2:
        if "Revenue" in financial.columns and financial["Revenue"].notna().any():
            revenue_fig = px.line(financial, x="Quarter", y="Revenue", title="Quarterly Revenue", markers=True)
            revenue_fig.update_traces(line=dict(color="#2ecc71", width=3), marker=dict(size=10))
            revenue_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
            st.plotly_chart(revenue_fig, use_container_width=True)

    financial_col1, financial_col2 = st.columns(2)

    with financial_col1:
        if "Assets" in financial.columns and financial["Assets"].notna().any():
            assets_fig = px.line(financial, x="Quarter", y="Assets", title="Total Assets", markers=True)
            assets_fig.update_traces(line=dict(color="#e74c3c", width=3), marker=dict(size=10))
            assets_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
            st.plotly_chart(assets_fig, use_container_width=True)

    with financial_col2:
        if "Liabilities" in financial.columns and financial["Liabilities"].notna().any():
            liabilities_fig = px.bar(financial, x="Quarter", y="Liabilities", title="Liabilities")
            liabilities_fig.update_traces(marker=dict(color="#e74c3c", line=dict(color="#e74c3c", width=2)))
            liabilities_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
            st.plotly_chart(liabilities_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 5. AVIATION AND MARKET COMPARISON
# =====================================================

st.header("5. Aviation & Market Comparison")

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
        )
    )
    comparison_trace_count += 1

if comparison_trace_count > 0:
    comparison_fig.update_layout(
        title="Indexed Performance Comparison",
        template="plotly_dark",
        height=500,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Indexed Return"
    )
    st.plotly_chart(comparison_fig, use_container_width=True)
else:
    st.warning("Comparison data could not be loaded.")

col1, col2 = st.columns(2)

with col1:
    if not pgsus.empty:
        pgsus_fig = px.line(pgsus, x="Date", y="close_price", title="PGSUS Stock Price")
        pgsus_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
        st.plotly_chart(pgsus_fig, use_container_width=True)

with col2:
    if not bist100.empty:
        bist_fig = px.line(bist100, x="Date", y="close_price", title="BIST 100 Index")
        bist_fig.update_layout(template="plotly_dark", height=400, plot_bgcolor="#16213e", paper_bgcolor="#0f1a2e", font=dict(color="#ecf0f1"), hovermode="x unified")
        st.plotly_chart(bist_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
---
### ✈️ HKV Team
Financial Management and Investment Dashboard Project

Developed with Streamlit & Plotly  

""")
