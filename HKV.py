import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from ta.trend import MACD
from ta.momentum import RSIIndicator
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

/* Tab Styling */
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

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%);
    border-right: 1px solid #2a5f8a;
}

/* Checkbox and Radio */
[data-testid="stCheckbox"] label, [data-testid="stRadio"] label {
    color: #bdc3c7 !important;
    font-weight: 600;
    transition: all 0.2s ease;
    cursor: pointer;
}

[data-testid="stCheckbox"] label:hover, [data-testid="stRadio"] label:hover {
    color: #ecf0f1 !important;
}

/* Selectbox Button */
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

/* Subheader */
[data-testid="stSubheaderMain"] {
    color: #bdc3c7;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* Smooth transitions for all interactive elements */
input, button, select, textarea {
    transition: all 0.2s ease;
}

input:focus, button:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #3498db !important;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1) !important;
}

/* Select text color */
p, label, span {
    color: #bdc3c7;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("✈️ HKV - THYAO Financial Dashboard")
st.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

thyao = pd.read_csv("data/thyao_price_yahoo_2020_2026.csv")

thyao['Date'] = pd.to_datetime(
    thyao['Date'],
    format='%d.%m.%Y'
)

gdp = pd.read_csv("data/gdp_growth_clean.csv")

gdp['Year'] = gdp['Year'].astype(str)

unemployment = pd.read_csv("data/unemployment.csv")

macro = pd.read_csv("data/macro_indicators.csv")
macro['Year'] = macro['Year'].astype(str)

financial = pd.read_csv("data/financial_metrics.csv")

budget = pd.read_csv("data/budget_balance.csv")
budget['Year'] = budget['Year'].astype(str)

current_account = pd.read_csv("data/current_account.csv")
current_account['Year'] = current_account['Year'].astype(str)

# =====================================================
# COLOR SCHEMES
# =====================================================

color_discrete = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"]
color_gradient = ["#3498db", "#2ecc71", "#e74c3c"]

close = thyao['close_price']

# RSI
rsi = RSIIndicator(close=close, window=14)
thyao['RSI'] = rsi.rsi()

# MACD
macd = MACD(close=close)

thyao['MACD'] = macd.macd()
thyao['MACD_SIGNAL'] = macd.macd_signal()

# Bollinger
bb = BollingerBands(close=close, window=20)

thyao['BB_HIGH'] = bb.bollinger_hband()
thyao['BB_LOW'] = bb.bollinger_lband()

# Moving Averages
thyao['MA20'] = close.rolling(window=20).mean()
thyao['MA50'] = close.rolling(window=50).mean()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("## ✈️ Dashboard Controls")

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(thyao['Date'].dt.year.unique())
)

chart_type = st.sidebar.radio(
    "Chart Type",
    ["Line", "Candlestick"]
)

show_volume = st.sidebar.checkbox(
    "Show Volume",
    value=True
)

show_ma = st.sidebar.checkbox(
    "Show Moving Averages",
    value=True
)

if selected_year != "All":
    thyao = thyao[thyao['Date'].dt.year == selected_year]

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("Overview Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Current Price",
    f"{thyao['close_price'].iloc[-1]:.2f} ₺"
)

col2.metric(
    "📈 Highest Price",
    f"{thyao['high'].max():.2f} ₺"
)

col3.metric(
    "📉 Lowest Price",
    f"{thyao['low'].min():.2f} ₺"
)

col4.metric(
    "📊 Average Volume",
    f"{thyao['volume'].mean():,.0f}"
)

st.markdown("---")

# =====================================================
# 1. MACRO ECONOMIC PANEL
# =====================================================

st.header("1. Macroeconomic Panel")

col1, col2 = st.columns(2)

with col1:

    st.subheader("GDP Growth")

    gdp_fig = px.line(
        gdp,
        x="Year",
        y="Growth",
        title="GDP Growth Trend",
        markers=True
    )

    gdp_fig.update_traces(line=dict(color="#3498db", width=3), marker=dict(size=10, color="#2ecc71"))
    gdp_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1", family="Segoe UI"),
        hovermode="x unified"
    )

    st.plotly_chart(gdp_fig, use_container_width=True)

with col2:

    st.subheader("Unemployment")

    unemployment_fig = px.line(
        unemployment,
        x="Year",
        y="Rate",
        title="Unemployment Trend"
    )

    unemployment_fig.update_traces(line=dict(color="#e74c3c", width=3), marker=dict(size=10))
    unemployment_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1", family="Segoe UI"),
        hovermode="x unified"
    )

    st.plotly_chart(unemployment_fig, use_container_width=True)

st.subheader("Macroeconomic Indicators")

macro_col1, macro_col2, macro_col3, macro_col4 = st.columns(4)

macro_col1.metric(
    "📊 Interest Rate",
    f"{macro['Interest_Rate'].iloc[-1]:.1f}%",
    f"{macro['Interest_Rate'].iloc[-1] - macro['Interest_Rate'].iloc[-2]:+.1f}%"
)

macro_col2.metric(
    "📈 Inflation",
    f"{macro['Inflation'].iloc[-1]:.1f}%",
    f"{macro['Inflation'].iloc[-1] - macro['Inflation'].iloc[-2]:+.1f}%"
)

macro_col3.metric(
    "💱 Exchange Rate",
    f"{macro['Exchange_Rate'].iloc[-1]:.2f} ₺",
    f"{macro['Exchange_Rate'].iloc[-1] - macro['Exchange_Rate'].iloc[-2]:+.2f}"
)

macro_col4.metric(
    "🏆 Gold Price",
    f"${macro['Gold_Price'].iloc[-1]:.0f}",
    f"{macro['Gold_Price'].iloc[-1] - macro['Gold_Price'].iloc[-2]:+.0f}"
)

macro_col1, macro_col2 = st.columns(2)

with macro_col1:

    interest_fig = px.line(
        macro,
        x="Year",
        y="Interest_Rate",
        title="Interest Rate Trend",
        markers=True
    )

    interest_fig.update_traces(line=dict(color="#3498db", width=3), marker=dict(size=10))
    interest_fig.update_layout(
        template="plotly_dark",
        height=350,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(interest_fig, use_container_width=True)

with macro_col2:

    inflation_fig = px.line(
        macro,
        x="Year",
        y="Inflation",
        title="Inflation Trend",
        markers=True
    )

    inflation_fig.update_traces(line=dict(color="#e74c3c", width=3), marker=dict(size=10))
    inflation_fig.update_layout(
        template="plotly_dark",
        height=350,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(inflation_fig, use_container_width=True)

macro_col1, macro_col2 = st.columns(2)

with macro_col1:

    kur_fig = px.line(
        macro,
        x="Year",
        y="Exchange_Rate",
        title="Exchange Rate Trend",
        markers=True
    )

    kur_fig.update_traces(line=dict(color="#3498db", width=3), marker=dict(size=10))
    kur_fig.update_layout(
        template="plotly_dark",
        height=350,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(kur_fig, use_container_width=True)

with macro_col2:

    gold_fig = px.line(
        macro,
        x="Year",
        y="Gold_Price",
        title="Gold Price Trend",
        markers=True
    )

    gold_fig.update_traces(line=dict(color="#f39c12", width=3), marker=dict(size=10))
    gold_fig.update_layout(
        template="plotly_dark",
        height=350,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(gold_fig, use_container_width=True)

macro_col1, macro_col2 = st.columns(2)

with macro_col1:

    current_fig = px.line(
        current_account,
        x="Year",
        y="Current_Account",
        title="Current Account Balance",
        markers=True
    )

    current_fig.update_traces(line=dict(color="#3498db", width=3), marker=dict(size=10))
    current_fig.update_layout(
        template="plotly_dark",
        height=350,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(current_fig, use_container_width=True)

with macro_col2:

    budget_fig = px.bar(
        budget,
        x="Year",
        y="Budget_Balance",
        title="Budget Balance",
        color="Budget_Balance",
        color_continuous_scale=["#FF6B9D", "#95a5a6", "#32CD32"]
    )

    budget_fig.update_layout(
        template="plotly_dark",
        height=350,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified",
        coloraxis_showscale=False
    )

    st.plotly_chart(budget_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 2. YIELD CURVE
# =====================================================

st.header("2. Yield Curve")

yield_data = pd.DataFrame({
    "Maturity": ["3M", "6M", "1Y", "2Y", "5Y", "10Y"],
    "Rate": [42, 41, 39, 36, 31, 28]
})

yield_fig = px.area(
    yield_data,
    x="Maturity",
    y="Rate",
    title="Yield Curve"
)

yield_fig.update_traces(fillcolor="rgba(52, 152, 219, 0.3)", line=dict(color="#3498db", width=3))
yield_fig.update_layout(
    template="plotly_dark",
    height=450,
    plot_bgcolor="#16213e",
    paper_bgcolor="#0f1a2e",
    font=dict(color="#ecf0f1"),
    hovermode="x unified"
)

st.plotly_chart(yield_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 3. THYAO STOCK PRICE
# =====================================================

st.header("3. THYAO Stock Price")

price_fig = go.Figure()

# Candlestick
if chart_type == "Candlestick":

    price_fig.add_trace(
        go.Candlestick(
            x=thyao['Date'],
            open=thyao['open'],
            high=thyao['high'],
            low=thyao['low'],
            close=thyao['close_price'],
            name='THYAO',
            increasing_line_color='#2ecc71',
            decreasing_line_color='#e74c3c'
        )
    )

# Line Chart
else:

    price_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['close_price'],
            mode='lines',
            name='Close Price',
            line=dict(width=3, color="#3498db")
        )
    )

# Moving Averages
if show_ma:

    price_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['MA20'],
            mode='lines',
            name='MA20',
            line=dict(color="#2ecc71", width=2, dash="dash")
        )
    )

    price_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['MA50'],
            mode='lines',
            name='MA50',
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

# Volume Chart
if show_volume:

    volume_fig = px.bar(
        thyao,
        x='Date',
        y='volume',
        title='Trading Volume'
    )

    volume_fig.update_traces(marker=dict(color="#3498db", line=dict(color="#3498db", width=1)))
    volume_fig.update_layout(
        template="plotly_dark",
        height=350,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(volume_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 4. TECHNICAL ANALYSIS
# =====================================================

st.header("4. Technical Analysis")

tab1, tab2, tab3 = st.tabs([
    "RSI",
    "MACD",
    "Bollinger Bands"
])

# RSI TAB
with tab1:

    rsi_fig = go.Figure()

    rsi_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color="#3498db", width=3)
        )
    )

    rsi_fig.add_hline(y=70, line_dash="dash", line_color="#e74c3c", annotation_text="Overbought")
    rsi_fig.add_hline(y=30, line_dash="dash", line_color="#2ecc71", annotation_text="Oversold")

    rsi_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(rsi_fig, use_container_width=True)

# MACD TAB
with tab2:

    macd_fig = go.Figure()

    macd_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color="#3498db", width=3)
        )
    )

    macd_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['MACD_SIGNAL'],
            mode='lines',
            name='Signal',
            line=dict(color="#2ecc71", width=2, dash="dash")
        )
    )

    macd_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(macd_fig, use_container_width=True)

# BOLLINGER TAB
with tab3:

    bollinger_fig = go.Figure()

    bollinger_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['close_price'],
            mode='lines',
            name='Close Price',
            line=dict(color="#3498db", width=3)
        )
    )

    bollinger_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['BB_HIGH'],
            mode='lines',
            name='Upper Band',
            line=dict(color="#e74c3c", dash="dash", width=2)
        )
    )

    bollinger_fig.add_trace(
        go.Scatter(
            x=thyao['Date'],
            y=thyao['BB_LOW'],
            mode='lines',
            name='Lower Band',
            line=dict(color="#2ecc71", dash="dash", width=2),
            fill='tonexty',
            fillcolor='rgba(46, 204, 113, 0.1)'
        )
    )

    bollinger_fig.update_layout(
        template="plotly_dark",
        height=450,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(bollinger_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 5. FINANCIAL METRICS
# =====================================================

st.header("5. Financial Metrics")

metric1, metric2, metric3, metric4 = st.columns(4)

latest_profit = financial['Profit'].iloc[-1]
latest_revenue = financial['Revenue'].iloc[-1]
latest_assets = financial['Assets'].iloc[-1]
prev_profit = financial['Profit'].iloc[-2]

metric1.metric(
    "💰 Profitability",
    f"₺{latest_profit:.1f}B",
    f"{((latest_profit - prev_profit) / prev_profit * 100):+.1f}%"
)

metric2.metric(
    "📊 Revenue",
    f"₺{latest_revenue:.1f}B"
)

metric3.metric(
    "🏢 Assets",
    f"₺{latest_assets:.1f}B"
)

metric4.metric(
    "📈 Beta",
    "1.12",
    "-0.05"
)

financial_col1, financial_col2 = st.columns(2)

with financial_col1:

    profit_fig = px.bar(
        financial,
        x="Quarter",
        y="Profit",
        title="Quarterly Profit"
    )

    profit_fig.update_traces(marker=dict(color="#3498db", line=dict(color="#3498db", width=2)))
    profit_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(profit_fig, use_container_width=True)

with financial_col2:

    revenue_fig = px.line(
        financial,
        x="Quarter",
        y="Revenue",
        title="Quarterly Revenue",
        markers=True
    )

    revenue_fig.update_traces(line=dict(color="#2ecc71", width=3), marker=dict(size=10))
    revenue_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(revenue_fig, use_container_width=True)

financial_col1, financial_col2 = st.columns(2)

with financial_col1:

    assets_fig = px.line(
        financial,
        x="Quarter",
        y="Assets",
        title="Total Assets",
        markers=True
    )

    assets_fig.update_traces(line=dict(color="#e74c3c", width=3), marker=dict(size=10))
    assets_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(assets_fig, use_container_width=True)

with financial_col2:

    liabilities_fig = px.bar(
        financial,
        x="Quarter",
        y="Liabilities",
        title="Liabilities"
    )

    liabilities_fig.update_traces(marker=dict(color="#e74c3c", line=dict(color="#e74c3c", width=2)))
    liabilities_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(liabilities_fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 6. AVIATION SECTOR
# =====================================================

st.header("6. Aviation Sector")

aviation_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Passengers": [5.2, 5.6, 6.1, 6.8, 7.0, 7.5],
    "Fuel Price": [780, 810, 790, 850, 890, 910],
    "Capacity": [82, 83, 85, 86, 87, 88],
    "Revenue": [125, 140, 155, 175, 185, 200]
})

avi_col1, avi_col2, avi_col3, avi_col4 = st.columns(4)

avi_col1.metric(
    "✈️ Passenger Count",
    f"{aviation_data['Passengers'].iloc[-1]:.1f}M",
    f"{aviation_data['Passengers'].iloc[-1] - aviation_data['Passengers'].iloc[-2]:+.1f}M"
)

avi_col2.metric(
    "⛽ Jet Fuel Price",
    f"${aviation_data['Fuel Price'].iloc[-1]:.0f}",
    f"{aviation_data['Fuel Price'].iloc[-1] - aviation_data['Fuel Price'].iloc[-2]:+.0f}"
)

avi_col3.metric(
    "📊 Capacity Utilization",
    f"{aviation_data['Capacity'].iloc[-1]:.0f}%",
    f"{aviation_data['Capacity'].iloc[-1] - aviation_data['Capacity'].iloc[-2]:+.0f}%"
)

avi_col4.metric(
    "💵 Monthly Revenue",
    f"₺{aviation_data['Revenue'].iloc[-1]:.0f}M",
    f"{aviation_data['Revenue'].iloc[-1] - aviation_data['Revenue'].iloc[-2]:+.0f}M"
)

col1, col2 = st.columns(2)

# Passenger Chart
with col1:

    passenger_fig = px.line(
        aviation_data,
        x="Month",
        y="Passengers",
        title="Passenger Count",
        markers=True
    )

    passenger_fig.update_traces(line=dict(color="#3498db", width=3), marker=dict(size=10))
    passenger_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(passenger_fig, use_container_width=True)

# Fuel Chart
with col2:

    fuel_fig = px.area(
        aviation_data,
        x="Month",
        y="Fuel Price",
        title="Jet Fuel Prices"
    )

    fuel_fig.update_traces(fillcolor="rgba(231, 76, 60, 0.3)", line=dict(color="#e74c3c", width=3))
    fuel_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(fuel_fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:

    capacity_fig = px.bar(
        aviation_data,
        x="Month",
        y="Capacity",
        title="Capacity Utilization (%)"
    )

    capacity_fig.update_traces(marker=dict(color="#2ecc71", line=dict(color="#2ecc71", width=2)))
    capacity_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(capacity_fig, use_container_width=True)

with col2:

    revenue_fig = px.line(
        aviation_data,
        x="Month",
        y="Revenue",
        title="Monthly Revenue",
        markers=True
    )

    revenue_fig.update_traces(line=dict(color="#3498db", width=3), marker=dict(size=10))
    revenue_fig.update_layout(
        template="plotly_dark",
        height=400,
        plot_bgcolor="#16213e",
        paper_bgcolor="#0f1a2e",
        font=dict(color="#ecf0f1"),
        hovermode="x unified"
    )

    st.plotly_chart(revenue_fig, use_container_width=True)

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