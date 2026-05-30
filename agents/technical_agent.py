import yfinance as yf


def technical_analysis(symbol):

    try:

        df = yf.download(
            tickers=symbol,
            period="3mo",
            interval="1d",
            progress=False,
            auto_adjust=True,
            threads=False
        )

        # EMPTY CHECK
        if df is None or df.empty:
            return {
                "error": "No technical data found"
            }

        # FIX MULTIINDEX
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        # CLOSE CHECK
        if "Close" not in df.columns:
            return {
                "error": "Close column missing"
            }

        close_series = df["Close"]

        sma_20 = close_series.tail(20).mean()

        latest_price = close_series.iloc[-1]

        trend = "Bullish"

        if latest_price < sma_20:
            trend = "Bearish"

        return {
            "latest_price": float(latest_price),
            "sma_20": float(sma_20),
            "trend": trend
        }

    except Exception as e:

        return {
            "error": str(e)
        }