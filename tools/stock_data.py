import yfinance as yf


def get_stock_data(symbol):

    try:

        df = yf.download(
            tickers=symbol,
            period="1mo",
            interval="1d",
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if df.empty:
            return {"error": "No data found"}

        # Fix MultiIndex issue
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        latest_close = df["Close"].values[-1]
        latest_volume = df["Volume"].values[-1]

        # Currency Detection
        currency = "INR" if symbol.upper().endswith(".NS") else "USD"

        return {
            "symbol": symbol,
            "current_price": float(latest_close),
            "volume": float(latest_volume),
            "currency": currency
        }

    except Exception as e:

        return {
            "error": str(e)
        }