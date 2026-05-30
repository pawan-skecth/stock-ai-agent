import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import re

from workflow.graph import app
from utils.supabase_memory import get_memory

st.set_page_config(
    page_title="Stock AI Agent",
    layout="wide"
)

st.title("🧠 Multi-Agent Stock AI System")

# =====================
# SESSION STATE
# =====================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "last_stock" not in st.session_state:
    st.session_state.last_stock = None

# =====================
# INPUTS
# =====================

stock = st.text_input("Enter Stock Symbol", "TSLA")

timeframe = st.selectbox(
    "📈 Select Chart Timeframe",
    ["Daily", "Weekly", "Monthly"]
)

# =====================
# ANALYZE BUTTON
# =====================

if st.button("Analyze"):

    with st.spinner("Running AI Agents..."):

        st.session_state.analysis_result = app.invoke({
            "stock_symbol": stock
        })

        st.session_state.last_stock = stock

# =====================
# SHOW RESULTS
# =====================

if st.session_state.analysis_result is not None:

    current_stock = st.session_state.last_stock

    # =====================
    # CHART SETTINGS
    # =====================

    interval = "1d"
    period = "6mo"

    if timeframe == "Weekly":
        interval = "1wk"
        period = "1y"

    elif timeframe == "Monthly":
        interval = "1mo"
        period = "5y"

    # =====================
    # CANDLESTICK CHART
    # =====================

    try:

        df = yf.download(
            current_stock,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False,
            threads=False
        )

        if not df.empty:

            if hasattr(df.columns, "levels"):
                df.columns = df.columns.get_level_values(0)

            st.subheader(
                f"📈 {current_stock.upper()} Candlestick Chart ({timeframe})"
            )

            df["SMA20"] = df["Close"].rolling(20).mean()

            fig = go.Figure()

            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="Candlestick"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SMA20"],
                    mode="lines",
                    name="SMA 20"
                )
            )

            fig.update_layout(
                height=600,
                xaxis_title="Date",
                yaxis_title="Price",
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Chart Error: {e}")

    # =====================
    # DECISION BADGE
    # =====================

    strategy_text = st.session_state.analysis_result["strategy"]

    decision = "HOLD"

    match = re.search(r"DECISION:\s*(BUY|HOLD|SELL)", strategy_text.upper())

    if match:
        decision = match.group(1)

    st.subheader("🎯 AI Recommendation")

    if decision == "BUY":
        st.success("🟢 BUY")

    elif decision == "SELL":
        st.error("🔴 SELL")

    else:
        st.warning("🟡 HOLD")

    st.subheader("📊 Final Decision")
    st.write(strategy_text)

    # =====================
    # MEMORY
    # =====================

    st.subheader("🧠 Past Decisions (Memory)")

    history = get_memory(current_stock)

    if history:
        for h in history:
            st.write(h)
    else:
        st.write("No memory found")

# =====================
# SIDEBAR
# =====================

st.sidebar.title("Agents Used")

st.sidebar.write("""
✔ Stock Data Tool  
✔ Fundamental Agent  
✔ Technical Agent  
✔ Risk Agent  
✔ News Agent  
✔ Sentiment Agent  
✔ Strategy Agent  
✔ Memory Agent (Supabase)
""")

# =====================
# 📋 AI INVESTMENT SUMMARY (IMPROVED)
# =====================

if st.session_state.analysis_result is not None:

    strategy_text = st.session_state.analysis_result["strategy"]

    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 AI Investment Summary")

    # Decision extraction
    if "BUY" in strategy_text.upper():
        recommendation = "🟢 BUY"
    elif "SELL" in strategy_text.upper():
        recommendation = "🔴 SELL"
    else:
        recommendation = "🟡 HOLD"

    st.sidebar.write("Recommendation:")
    st.sidebar.success(recommendation)

    st.sidebar.write("---")
    st.sidebar.write("Quick Insight:")

    insights = []

    if "overvalued" in strategy_text.lower():
        insights.append("⚠️ Stock appears overvalued")

    if "bullish" in strategy_text.lower():
        insights.append("📈 Bullish technical trend")

    if "bearish" in strategy_text.lower():
        insights.append("📉 Bearish technical trend")

    if "low risk" in strategy_text.lower():
        insights.append("🛡️ Low risk level")

    if "neutral" in strategy_text.lower():
        insights.append("⚖️ Neutral market sentiment")

    if len(insights) == 0:
        insights.append("Market conditions are mixed or unclear")

    for i in insights:
        st.sidebar.write(i)

    st.sidebar.write("---")
    st.sidebar.write("Summary:")

    if recommendation == "🟢 BUY":
        st.sidebar.write("Strong positive signals detected across multiple agents.")
    elif recommendation == "🔴 SELL":
        st.sidebar.write("Risk factors dominate over positive signals.")
    else:
        st.sidebar.write("Conflicting signals. Best to monitor before taking action.")